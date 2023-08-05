# -*- coding:utf-8
import numpy as np
from itertools import chain
import shelve
import glob
import numpy as np
import time
import os
import re
import functools
from multiprocessing import Pool
from collections import defaultdict, Counter
from multiprocessing import Pool, cpu_count
from ..tools import SplitFile, ArrayDict, ArrayList
# from ..ctools import ArrayListFromTo as ArrayList
# from numba import jit
import json

# HASH_SHORT = 64
NODE_TYPE_MASK = 2**60 - 1
# @jit(nopython=True)
def chash(t, s): 
#     return hash(s)
    return t | (hash(s) & NODE_TYPE_MASK)
    # return hash(t + s)
    # return hash(t + s)

def lines_sampler(relationship_files):
    ''' 对图数据集做采样统计, 供后续估计hash空间使用, 提升导入效率
    '''
    key_sample_lines, nodes_line_num = defaultdict(list), defaultdict(int)
    for relation in relationship_files:
        relation, basename = os.path.abspath(relation), os.path.basename(relation)
        with open(relation) as f:
            l = f.readline()
            from_col, to_col = re.findall("\((.+?)\)", l)
        splitfiles = SplitFile.split(relation, num=200, jump=1)
        filesize = os.path.getsize(relation)
        def sample_lines(sfs, cnt=1000):
            for arg in sfs:
                sf, i = SplitFile(*arg), 0
                for l in sf: 
                    if i > cnt: break
                    yield l
                    i += 1
        lines = list(sample_lines(splitfiles))
        for l in lines:
            keys = l.replace("\n", "").split(",")
            if len(keys) != 3:
                continue
            key_sample_lines[from_col].append(keys[0])
            key_sample_lines[to_col].append(keys[1])
        line_len_mean = np.mean(list(map(lambda l:len(l.encode('utf-8')), lines)))
        line_num = int(filesize / line_len_mean)
        nodes_line_num[from_col] += line_num
        nodes_line_num[to_col] += line_num
    return key_sample_lines, nodes_line_num

def node_hash_space_stat(key_sample_lines, nodes_line_num,
            without_freq=False,
            HID_BATCH_SIZE_AVERAGE=int(5e6), 
            FREQ_WORDS_TOP_KEEP=10, 
            FREQ_WORDS_TOP_RATIO=0.01):
    ''' 根据数据集的分布情况自动切分hash空间和高频节点列表
    '''
    NODES_SHORT_HASH, freq_nodes = {}, {}
    for node, l in nodes_line_num.items():
        NODES_SHORT_HASH[node] = l // HID_BATCH_SIZE_AVERAGE
    if without_freq:
        return freq_nodes, NODES_SHORT_HASH

    for node, words in key_sample_lines.items():
        node_freq_word_cnt = Counter(words).most_common(FREQ_WORDS_TOP_KEEP)
        csum = len(words)
        topstat = [(node, fcnt, fcnt / csum) for node, fcnt in node_freq_word_cnt]
        freqitem = list(filter(lambda x: x[2] > FREQ_WORDS_TOP_RATIO, topstat))
        freqrate = sum([e[-1] for e in freqitem])
        # HASH空间切分数 = 非高频节点的记录数 / 期望的hash batch大小
        NODES_SHORT_HASH[node] = int(nodes_line_num[node] * (1 - freqrate)) // HID_BATCH_SIZE_AVERAGE 
        # 建立节点高频word集合
        if len(freqitem) > 0:
            freq_nodes[node] = set([chash(Context.node_type_hash(node), item[0]) for item in freqitem])
    return freq_nodes, NODES_SHORT_HASH

class Context:
    NODE_TYPE = {}
    NODE_FILE = {}
    node_type_path = None
    node_file_path = None

    @staticmethod
    def prepare_nodes(node_files):
        for fn in node_files:
            Context.node_file_hash(fn)
        with open(Context.node_file_path, "w") as f:
            f.write(json.dumps(Context.NODE_FILE))
        pass
    
    @staticmethod
    def prepare_relations(relation_files):
        for fn in relation_files:
            with open(fn) as f:
                FROM_COL, TO_COL = re.findall("\((.+?)\)", f.readline())
                Context.node_type_hash(FROM_COL)
                Context.node_type_hash(TO_COL)
        with open(Context.node_type_path, "w") as f:
            f.write(json.dumps(Context.NODE_TYPE))
    
    @staticmethod
    def node_type_hash(col):
        if col in Context.NODE_TYPE:
            return Context.NODE_TYPE[col]
        else:
            Context.NODE_TYPE[col] = len(Context.NODE_TYPE) << 60 
            return Context.NODE_TYPE[col]
    
    @staticmethod
    def node_file_hash(filename):
        # 给定文件路径返回对应fid
        # 单文件2**45 = 100G， 文件上限个数2**19 = 524288个 （ext3 inode 默认 个数上限）
        if filename in Context.NODE_FILE:
            return Context.NODE_FILE[filename]
        else:
            Context.NODE_FILE[filename] = len(Context.NODE_FILE) << (64 - 19)
            return Context.NODE_FILE[filename]
    
    
    @staticmethod
    @functools.lru_cache()
    def node_file(fid):
        filename = Context.NODE_FILE.get(fid, None)
        if filename is None:
            return None
        return open(filename)
        pass
        
    @staticmethod
    def load_node_type_hash(path):
        Context.node_type_path = path
        if not os.path.exists(Context.node_type_path):
            os.makedirs(os.path.dirname(Context.node_type_path), exist_ok=True)
            Context.NODE_TYPE = {}
            return
        Context.NODE_TYPE = json.loads(open(Context.node_type_path, "r").read())
        
    @staticmethod
    def load_node_file_hash(path):
        Context.node_file_path = path
        if not os.path.exists(Context.node_file_path):
            os.makedirs(os.path.dirname(Context.node_file_path), exist_ok=True)
            Context.NODE_FILE = {}
            return
        Context.NODE_FILE = json.loads(open(Context.node_file_path, "r").read())

import time
import random
# @jit(nopython=True)
def lines2idxarr(output, splitfile_arguments, chunk_id, freq_nodes, NODES_SHORT_HASH):
    # output, (path, _from, _to), chunk = args
    with open(splitfile_arguments[0]) as f:
        FROM_COL, TO_COL = re.findall("\((.+?)\)", f.readline())
        FROM_COL_HASH, TO_COL_HASH = Context.node_type_hash(FROM_COL), Context.node_type_hash(TO_COL)
    # FROM_SHORT_HASH, TO_SHORT_HASH = NODES_SHORT_HASH[FROM_COL], NODES_SHORT_HASH[TO_COL]
    # 固定为64的原因主要还是考虑后续会映射到edge dict中, 统一使用64bin去切割
    FROM_SHORT_HASH, TO_SHORT_HASH, SHORT_HASH_MASK = 64, 64, (1 << 6) - 1
    
    splitfile = SplitFile(*splitfile_arguments)
    os.makedirs(output, exist_ok=True)
    # 随机块大小是为了让进程吃资源的节奏错开
    random_chunk_size = lambda : random.randint(300000, 600000)
    # 针对非高频节点使用使用短hash映射到共享空间，需要独立重排
    from_node_lists = [ArrayList("%s/hid_%d_%s.idxarr.chunk_%d" % \
                        (output, i, FROM_COL, chunk_id), 
                        chunk_size=random_chunk_size(),
                      dtype=[('from', np.int64), ('to', np.int64), ('ts', np.int32)]) 
              for i in range(FROM_SHORT_HASH)]
    to_node_lists = [ArrayList("%s/hid_%d_%s.idxarr.chunk_%d" % \
                        (output, i, TO_COL, chunk_id), 
                        chunk_size=random_chunk_size(),
                      dtype=[('from', np.int64), ('to', np.int64), ('ts', np.int32)]) 
              for i in range(TO_SHORT_HASH)]
    # 针对高频节点， 使用独立的空间， 不需要重排
    freq_output = f"{output}/freq_edges"
    os.makedirs(freq_output, exist_ok=True)
    ffdict_able_flag, tfdict_able_flag = False, False
    if FROM_COL in freq_nodes: 
        from_node_freq_dict = {fk:ArrayList("%s/hid_%s_%s.idxarr.chunk_%d" % \
                            (freq_output, str(fk), FROM_COL, chunk_id), 
                               chunk_size=random_chunk_size(),
                          dtype=[('to', np.int64), ('ts', np.int32)]) 
                        #   dtype=[('from', np.int64), ('to', np.int64)]) 
                  for fk in list(freq_nodes[FROM_COL])}
        from_node_freq_dict_set = set(from_node_freq_dict.keys())
        ffdict_able_flag = True
    if TO_COL in freq_nodes:
        to_node_freq_dict = {tk:ArrayList("%s/hid_%s_%s.idxarr.chunk_%d" % \
                            (freq_output, str(tk), TO_COL, chunk_id), 
                               chunk_size=random_chunk_size(),
                          dtype=[('to', np.int64), ('ts', np.int32)]) 
                        #   dtype=[('from', np.int64), ('to', np.int64)]) 
                  for tk in list(freq_nodes[TO_COL])}
        to_node_freq_dict_set = set(to_node_freq_dict.keys())
        tfdict_able_flag = True
            
    for line in splitfile:
        # from_str, to_str
        r = line[:-1].split(",")
        if len(r) != 3:
            continue
        try:
            h1, h2, ts = chash(FROM_COL_HASH, r[0]), chash(TO_COL_HASH, r[1]), int(r[2])
        except ValueError:
            continue
        # 记录高频节点, 自动双向
        if ffdict_able_flag and (h1 in from_node_freq_dict_set):
            from_node_freq_dict[h1].append((h2, ts))
        else: # 记录非高频节点
#             from_node_lists[h1 // 0xf % FROM_SHORT_HASH].append((h1, h2))
            from_node_lists[h1 & SHORT_HASH_MASK].append((h1, h2, ts))
            
        if tfdict_able_flag and (h2 in to_node_freq_dict_set):
            to_node_freq_dict[h2].append((h1, ts))
        else:
#             to_node_lists[h2 // 0xf % TO_SHORT_HASH].append((h2, h1))
            to_node_lists[h2 & SHORT_HASH_MASK].append((h2, h1, ts))
    # 将arraylist数据flush到磁盘中
    for arraylist in from_node_lists + to_node_lists: 
        arraylist.close(merge=False)
    if ffdict_able_flag:
        for arraylist in from_node_freq_dict.values():
            arraylist.close(merge=False)
    if tfdict_able_flag:
        for arraylist in to_node_freq_dict.values():
            arraylist.close(merge=False)

# dataset = "/data_ssd/workspace/hp/dataset"
# graph = '/data_ssd/workspace/hp/graph'

def relationship2indexarray(dataset, graph, CHUNK_COUNT = cpu_count()):
    key_sample_lines, nodes_line_num = lines_sampler(glob.glob(f"{dataset}/relation_*.csv"))
    freq_nodes, NODES_SHORT_HASH = node_hash_space_stat(key_sample_lines, nodes_line_num)
    pool = Pool(processes=CHUNK_COUNT)
    for relation in glob.glob(f"{dataset}/relation_*.csv"):
        relation, basename = os.path.abspath(relation), os.path.basename(relation)
        start_time = time.time()
        print("## Relationship to index array transforming... ##", relation)
        
#         for args in [(f"{graph}/{basename}.idxarr", 
#                 splitfile_arguments, 
#                 chunk_id, 
#                 freq_nodes, 
#                 NODES_SHORT_HASH) for chunk_id, 
#                     splitfile_arguments in 
#                     enumerate(SplitFile.split(relation, num=CHUNK_COUNT, jump=1))][:1]:
#             lines2idxarr(*args)
        pool.starmap(lines2idxarr,
            [(f"{graph}/{basename}.idxarr", 
                splitfile_arguments, 
                chunk_id, 
                freq_nodes, 
                NODES_SHORT_HASH) for chunk_id, 
                    splitfile_arguments in 
                    enumerate(SplitFile.split(relation, num=CHUNK_COUNT, jump=1))])
        print("Time usage:", time.time() - start_time)
    


def merge_mem_array(mems):
    ''' 合并 memmap
    '''
    assert len(mems) > 0
    arr = np.zeros(shape=(sum([m.shape[0] for m in mems]), ), dtype=mems[0].dtype)
    cur = 0
    for m in mems:
        arr[cur:cur + m.shape[0]] = m
        cur += m.shape[0]
    return arr

# @jit(nopython=True)
def unique_inplace(arr, unique=None, order=None, axis=0, kind='mergesort'):
    # memmap sort inplaced then unique index & counts return
    arr.sort(order=order, axis=axis, kind=kind)
    return np.unique(arr[unique], return_index=True, return_counts=True)

import glob
def hid_idx_dict(graph, _id):
    # 所有short hid为_id的节点(不区分节点类型)索引全部都放入同一个字典中
    idxarr = [np.memmap(f, 
                     mode='r', 
                     dtype=[('value', np.int64), 
                         ('index', np.int64), 
                         ('length', np.int32)])
                 for f in glob.glob(f"{graph}/edges_sort/hid_%d_*.idx.arr" % _id)]
    freqarr = np.memmap(f"{graph}/edges_sort/hid_freq.idx.arr", 
                     mode='r', 
                     dtype=[('value', np.int64), 
                         ('index', np.int64), 
                         ('length', np.int32)])
    edges_index_count_sum = sum([i.shape[0] for i in idxarr])
    os.makedirs(f"{graph}/edges_mapper", exist_ok=True)
    adict = ArrayDict(memmap_path=f"{graph}/edges_mapper/hid_%d.dict.arr" % _id, 
                      memmap=True,
                      item_size=edges_index_count_sum, 
                      hash_heap_rate=0.5, 
                      value_dtype=[('index', np.int64), ('length', np.int32)], 
                      memmap_mode='w+')
    
    for _id, ia in enumerate(idxarr):
        adict[ia['value']] = ia[['index', 'length']]
    # freq部分实际上是被重复写入到全部 hash short_dict中了
    adict[freqarr['value']] = freqarr[['index', 'length']]

def hid_idx_merge(graph):
    p = Pool(processes=cpu_count())
    stime = time.time()
    res = p.starmap(hid_idx_dict, [(graph, i) for i in range(64)])
    print(time.time() - stime)

class MergeIndex:
    import numpy as np
    import time
    edge_to_cursor = 0
    toarrconcat: np.memmap = None
    freq_idx_pointer = {}
    @staticmethod
    def merge_idx_to(k, ipts):
        '''
        '''
        mems = [np.memmap(f, mode='r', dtype=[('from', np.int64), ('to', np.int64), ('ts', np.int32)]) 
                for f in ipts]
        arr = merge_mem_array(mems)
        _val, _idx, _len = unique_inplace(arr, unique='from', order=['from', 'ts'])
        return k, ipts, arr, _val, _idx, _len


    @staticmethod
    def merge_idx_to_callback(args):
        k, ipts, arr, _val, _idx, _len = args
#         print(ipts[0])
        graph = "/" + "/".join(ipts[0].split("/")[:-2])
        idxarr = np.memmap(f"{graph}/edges_sort/{k}.idx.arr", 
            mode='w+',
            order='F',
            shape=(_val.shape[0], ), 
            dtype=[('value', np.int64), 
                    ('index', np.int64), 
                    ('length', np.int32)])
        idxarr['value'] = _val
        idxarr['index'] = _idx + MergeIndex.edge_to_cursor
        idxarr['length'] = _len
        
        MergeIndex.toarrconcat[MergeIndex.edge_to_cursor: MergeIndex.edge_to_cursor + arr.shape[0]]['value'] = arr['to']
        MergeIndex.toarrconcat[MergeIndex.edge_to_cursor: MergeIndex.edge_to_cursor + arr.shape[0]]['ts'] = arr['ts']
        MergeIndex.toarrconcat[MergeIndex.edge_to_cursor: MergeIndex.edge_to_cursor + arr.shape[0]]['index'] = arr['from']
        MergeIndex.edge_to_cursor += arr.shape[0]

    @staticmethod
    def merge_freq_idx_to(k, ipts):
        # 针对高频节点边表merge处理
        mems = [np.memmap(f, mode='r', dtype=[('to', np.int64), ('ts', np.int32)]) 
                for f in ipts]
        return k, mems
        pass

    @staticmethod
    def merge_freq_idx_to_callback(args):
        # 针对高频节点边表merge处理，回调
        k, mems = args
        value = k
        index = MergeIndex.edge_to_cursor
        length = sum([m.shape[0] for m in mems])
        MergeIndex.freq_idx_pointer[value] = (index, length)
        for m in mems:
            MergeIndex.toarrconcat[MergeIndex.edge_to_cursor: MergeIndex.edge_to_cursor + m.shape[0]]['value'] = m['to']
            MergeIndex.toarrconcat[MergeIndex.edge_to_cursor: MergeIndex.edge_to_cursor + m.shape[0]]['ts'] = m['ts']
            MergeIndex.toarrconcat[MergeIndex.edge_to_cursor: MergeIndex.edge_to_cursor + m.shape[0]]['index'] = k
            MergeIndex.edge_to_cursor += m.shape[0]
        pass

    @staticmethod
    def freq_idx_pointer_dump(graph):
        # 针对高频节点->边索引表的处理
        idxarr = np.memmap(f"{graph}/edges_sort/hid_freq.idx.arr", 
            mode='w+',
            order='F',
            shape=(len(MergeIndex.freq_idx_pointer), ), 
            dtype=[('value', np.int64), 
                    ('index', np.int64), 
                    ('length', np.int32)])

        for idx, (value, (index, length)) in enumerate(MergeIndex.freq_idx_pointer.items()):
            idxarr[idx]['value'] = value
            idxarr[idx]['index'] = index
            idxarr[idx]['length'] = length
            pass
        
def merge_index_array_then_sort(graph):
    import glob
    from collections import defaultdict
    # chunk split
    chunk_files = list(glob.glob(f"{graph}/*.idxarr/hid_*_*.idxarr.chunk*"))
    freq_files = list(glob.glob(f"{graph}/*.idxarr/freq_edges/hid_*.chunk*"))
    files_hash_dict = defaultdict(list)
    files_freq_dict = defaultdict(list)
    for cfile in chunk_files:
        hash_id = re.findall(".*/(.+?).idxarr*", cfile)[0]
        files_hash_dict[hash_id].append(cfile)
    for ffile in freq_files:
        fname = os.path.basename(ffile)
        fid = int(fname.split('_')[1])
        files_freq_dict[fid].append(ffile) 

    edges_count_sum = sum([np.memmap(f, mode='r', dtype=[('from', np.int64), ('to', np.int64), ('ts', np.int32)]).shape[0] 
                for f in sum(list(files_hash_dict.values()), [])])
    edges_count_sum += sum([np.memmap(f, mode='r', dtype=[('to', np.int64), ('ts', np.int32)]).shape[0] 
                for f in sum(list(files_freq_dict.values()), [])])

    os.makedirs(f"{graph}/edges_sort", exist_ok=True)
    MergeIndex.edge_to_cursor = 0
    MergeIndex.toarrconcat = np.memmap(f"{graph}/concat.to.arr", 
            mode='w+',
            shape=(edges_count_sum, ), 
            order='F',
            dtype=[('index', np.int64), ('value', np.int64), ('ts', np.int32)])

    pool = Pool(processes=cpu_count())
    stime = time.time()
    for items in list(files_hash_dict.items()):
        pool.apply_async(MergeIndex.merge_idx_to, 
            args=items, 
            callback=MergeIndex.merge_idx_to_callback)
    for items in list(files_freq_dict.items()):
        pool.apply_async(MergeIndex.merge_freq_idx_to,
            args=items,
            callback=MergeIndex.merge_freq_idx_to_callback)
    pool.close()
    pool.join()
    MergeIndex.freq_idx_pointer_dump(graph)
    print(time.time() - stime)


RES_64_MASK = (1 << 6) - 1
class HashSplitDict():
    def __init__(self, path, dtype=np.int32, hlen=64, item_get_cursor=False):
        self.dtype = dtype
        self.hlen = hlen
        self.item_get_cursor = item_get_cursor
        self.hdict_start_idx = {}
        self.hdict = self._load(path)
        
        
    
    def _load(self, path):
        r = {}
        hdict_start_idx_cursor = 0
        for i in range(self.hlen):
            r[i] = ArrayDict(memmap_path=f"{path}/hid_%d.dict.arr" % i, 
                  memmap=True,
                  value_dtype=self.dtype, 
                  memmap_mode='r',
                 item_get_cursor=self.item_get_cursor)
            self.hdict_start_idx[i] = hdict_start_idx_cursor
            hdict_start_idx_cursor = r[i].HEAP.shape[0]
        return r
    
    def __setitem__(self, key, value):
#         _id = key % self.hlen
        _id = key & RES_64_MASK
        for i in np.unique(_id):
            idx = (_id == i)
            self.hdict[i][key[idx]] = value[idx]
        pass
    
    def __getitem__(self, key):
        ret = np.zeros_like(key, dtype=self.dtype)
        if self.item_get_cursor:
            ret_cursor = np.zeros_like(key, dtype=np.int32)
#         _id = key % self.hlen
        _id = key & RES_64_MASK
        for i in np.unique(_id):
            idx = (_id == i)
            if self.item_get_cursor:
                ret[idx], ret_cursor[idx] = self.hdict[i][key[idx]]
                ret_cursor[idx] += self.hdict_start_idx[i]
            else:
                ret[idx] = self.hdict[i][key[idx]]
        if self.item_get_cursor:
            return ret, ret_cursor
        return ret
    
def sample_neibor(toarr, hsd, seed):
    idx = hsd[seed]
    return toarr[np.unique(np.hstack([np.arange(i, i + l) for i, l in idx]))]['value']

import pickle
sample_length = 0
sampler_length = 0
def graph_sampler(_seeds, deep, neibor, toarr, mapper):
    global sample_length
    global sampler_length
    if deep == 0:
        return [_seeds]
    # seeds_diff = np.setdiff1d(_seeds, seeds_exist)
    layer_seeds = graph_sampler(_seeds, deep - 1, neibor, toarr, mapper)
    seeds = layer_seeds[-1]
    # type过滤
    seeds = seeds[seeds >> 60 & 0b01 == 0b01]
#     print(seeds, layer_seeds)
    idx = mapper[seeds]
    
#     print("B:", seeds,idx, (idx['length'] > 0).sum())
    idx = idx[idx['length'] > 0]
    def sample_range(_from, _len, neibor_cnt):
        if _len > neibor_cnt:
            return np.random.randint(_from, _from + _len, neibor_cnt)
        else:
            return np.arange(_from, _from + _len)
    R = [sample_range(_f,  _l, neibor)
                        for _f, _l in idx]
#     print('#', seeds, idx)
    stack = np.hstack(R)
    index = np.unique(stack)
    sample_length += index.shape[0]
    sampler_length += 1
    nodes = toarr[index]#['value']
    return layer_seeds + [nodes]





# zip([re.findall("(.+?).idxarr*", f)[0] for f in fs], fs))

# import argparse
# parser = argparse.ArgumentParser()
# parser.parse_args()

import sys

def test(a, seed):
    global toarrconcat
    global hsd
    bs = graph_sampler(seed, int(sys.argv[4]), int(sys.argv[5]), toarrconcat, hsd)
    return bs

toarrconcat = None
hsd = None
def main():
    global toarrconcat
    global hsd
    '''python3 -m litegraph.importer.importer /data_ssd/workspace/hp/dataset /data_ssd/workspace/hp/graph
    python3 -m litegraph.importer.importer /data/dataset /data/graph 3 800
    echo 1 > /proc/sys/vm/drop_caches;python3 -m litegraph.importer.importer /data_ssd/workspace/hp/dataset_lite /data_ssd/workspace/hp/graph_lite 5 10 
    '''
    stime = time.time()
    print("T1:", stime)
    dataset, graph = sys.argv[1], sys.argv[2]
    Context.load_node_type_hash(f"{graph}/node_type_id.json")
    Context.load_node_file_hash(f"{graph}/node_file_id.json")
    Context.prepare_relations(glob.glob(f"{dataset}/relation_*.csv"))
    Context.prepare_nodes(glob.glob(f"{dataset}/node_*.csv"))
        
    print(f"Dataset: {dataset}\nGraph: {graph}")
    if False or (int(sys.argv[3]) & 0x01): # Dump edge test
        print("Relationship Index Transforming...")
        relationship2indexarray(dataset, graph)
        print(f"Index resorted to edge mergeing...")
        merge_index_array_then_sort(graph)
        print(f"Graph index merge by hashid...")
        hid_idx_merge(graph)
        print("Merge success")
    
    if False or (int(sys.argv[3]) & 0x02): # Dump node test
        print(f"Node to hashid transforming...")
        node2indexarray(dataset, graph)
        print(f"Node index mapping...")
        merge_node_index(graph)
    

    etime = time.time()
    print("T2:", etime)
    print("DT:", (etime - stime) / 60)
    
    if False or (int(sys.argv[3]) & 0x04): # Sampler test
        toarrconcat = np.memmap(f"{graph}/concat.to.arr", 
            mode='r',
            dtype=[('value', np.int64)])['value']

        hsd = HashSplitDict(f"{graph}/edges_mapper", 
                        dtype=[('index', np.int64), 
                               ('length', np.int32)], 
                        hlen=64)
        '''
        Benchmark:
        12T 6 10 10 1761w 5.6s
        12T 5 10 100 2546w 8s 
        1T 5 10 100 220w 4s
        1T 5 10 5 10w 0.5s
        12T 5 10 5 137w 0.9s
        '''
        seed = toarrconcat[np.random.randint(0, toarrconcat.shape[0], int(sys.argv[6]))]
        print(time.time())
        stime = time.time()
#         test(1, seed)
        pool = Pool(processes=cpu_count())
        res = pool.starmap(test, [(_, toarrconcat[np.random.randint(0, toarrconcat.shape[0], int(sys.argv[6]))]) for _ in range(12)])
        pool.close()
        pool.join()
        print(sample_length, sampler_length)
        print(time.time() - stime)
        print(sum([bs[-1].shape[0] for bs in res]), [[b.shape for b in bs] for bs in res])
        
        
    pass
   
def fuzzy_word_count(path):
    '''替代 wc -l 的统计估计方法
    '''
    splitfiles = SplitFile.spilt(path, 1000)
    line_size = np.mean([len(s.read()) for s in splitfiles])
    file_size = os.path.getsizeof(path)
    line_count = file_size // line_size
    return line_count
    
def node_importer(node_path, _type, graph):
    node_hash_index = ArrayDict(f"{graph}/node_index/node_{_type}.index.arr", 
                                size = fuzzy_word_count(path), 
                                rate = 0.7)
    cursor = 0
    for l in open(node_path):
        node_hash_index[hash(l) << 4 | _type_index] = cursor
        cursor += len(l)
    return node

node_indexs = {}
node_files = {}
def node_fetch(_type, node_hash):
    '''node索引取内容
    '''
    global node_indexs
    cursor = node_indexs[_type][node_hash]
    node_files[_type].seek(cursor)
    return node_files[_type].readline()

def node2idxarr(output, splitfile_arguments, chunk_id):
    output = f"{output}"
    os.makedirs(output, exist_ok=True)
    with open(splitfile_arguments[0]) as f:
        l = f.readline()
        NODE_COL, = re.findall("\((.+?)\)", l)
        NODE_FILE_HASH = Context.node_file_hash(splitfile_arguments[0])
        NODE_COL_HASH = Context.node_type_hash(NODE_COL)
    # FROM_SHORT_HASH, TO_SHORT_HASH = NODES_SHORT_HASH[FROM_COL], NODES_SHORT_HASH[TO_COL]
    # 固定为64的原因主要还是考虑后续会映射到edge dict中, 统一使用64bin去切割
    NODE_SHORT_HASH, SHORT_HASH_MASK = 64, (1 << 6) - 1
    random_chunk_size = lambda : random.randint(300000, 600000)
    splitfile = SplitFile(*splitfile_arguments)
    node_cursor_lists = [ArrayList("%s/hid_%d_%s.curarr.chunk_%d" % \
                    (output, i, NODE_COL, chunk_id), 
                    chunk_size=random_chunk_size(),
                  dtype=[('nid', np.int64), ('cursor', np.int64)]) 
          for i in range(NODE_SHORT_HASH)]
    _l = next(splitfile)
    cursor = len(_l)
    for l in splitfile:
        seg = l[:-1].split(",")
        nid = chash(NODE_COL_HASH, seg[0])
        node_cursor_lists[nid & SHORT_HASH_MASK].append((nid, NODE_FILE_HASH | cursor))
        cursor += len(l)
    
    for arraylist in node_cursor_lists: 
        arraylist.close(merge=False)
    pass

def node2indexarray(dataset, graph, CHUNK_COUNT = cpu_count()):
    
#     for nodefile in glob.glob(f"{dataset}/node_event_id.csv"):
#         nodefile, basename = os.path.abspath(nodefile), os.path.basename(nodefile)
#         start_time = time.time()
#         print("## Node to index array transforming... ##", nodefile)
#         for chunk_id, splitfile_arguments in \
#             enumerate(SplitFile.split(nodefile, num=CHUNK_COUNT, jump=1)):
#             node2idxarr(f"{graph}/{basename}.idxarr", splitfile_arguments, chunk_id)
    pool = Pool(processes=CHUNK_COUNT)
    for nodefile in glob.glob(f"{dataset}/node_*.csv"):
        nodefile, basename = os.path.abspath(nodefile), os.path.basename(nodefile)
        start_time = time.time()
        print("## Node to index array transforming... ##", nodefile)
        pool.starmap(node2idxarr,
            [(f"{graph}/{basename}.curarr", 
                splitfile_arguments, 
                chunk_id) for chunk_id, 
                    splitfile_arguments in 
                    enumerate(SplitFile.split(nodefile, num=CHUNK_COUNT, jump=1))])
        print("Time usage:", time.time() - start_time)


def merge_node_cursor_dict(graph, _id):
    # 所有short hid为_id的节点(不区分节点类型)索引全部都放入同一个字典中
    idxarr = [np.memmap(f, 
                     mode='r', 
                     dtype=[('idx', np.int64), 
                         ('cursor', np.int64)])
                 for f in glob.glob(f"{graph}/node_*.csv.curarr/hid_%d_*.curarr.chunk*" % _id)]
    nodes_cursor_sum = sum([i.shape[0] for i in idxarr])
    os.makedirs(f"{graph}/nodes_mapper", exist_ok=True)
    adict = ArrayDict(memmap_path=f"{graph}/nodes_mapper/hid_%d.dict.arr" % _id, 
                      memmap=True,
                      item_size=nodes_cursor_sum, 
                      hash_heap_rate=0.5, 
                      value_dtype=[('cursor', np.int64)], 
                      memmap_mode='w+')
    
    for _id, ia in enumerate(idxarr):
        adict[ia['idx']] = ia['cursor']
        
def merge_node_index(graph):
    p = Pool(processes=cpu_count())
    stime = time.time()
    res = p.starmap(merge_node_cursor_dict, [(graph, i) for i in range(64)])
    print(time.time() - stime)
    
    pass

if __name__ == "__main__":
    main()




    
    
    
    
    
    
    
    