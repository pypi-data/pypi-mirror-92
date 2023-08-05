# -*- coding:utf-8
import numpy as np
from itertools import chain
import glob
import numpy as np
import time
import os
import re
from multiprocessing import Pool
from collections import defaultdict, Counter
from multiprocessing import Pool, cpu_count
from ..tools import SplitFile, ArrayDict, ArrayList
# from ..tools import ArrayListFromTo as ArrayList

# HASH_SHORT = 64

def lines_sampler(relationship_files):
    ''' 对图数据集做采样统计, 供后续估计hash空间使用, 提升导入效率
    '''
    key_sample_lines, nodes_line_num = defaultdict(list), defaultdict(int)
    for relation in relationship_files:
        relation, basename = os.path.abspath(relation), os.path.basename(relation)
        with open(relation) as f:
            from_col, to_col = re.findall("\((.+?)\)", f.readline())
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
            if len(keys) != 2:
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

    node_type_index = 0; # random TODO modify
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
            freq_nodes[node] = set([hash(item[0]) << 4 | node_type_index for item in freqitem])
    return freq_nodes, NODES_SHORT_HASH


import time
import random
# @profile
def lines2idxarr(output, splitfile_arguments, chunk_id, freq_nodes, NODES_SHORT_HASH):
    # output, (path, _from, _to), chunk = args
    with open(splitfile_arguments[0]) as f:
        FROM_COL, TO_COL = re.findall("\((.+?)\)", f.readline())
    # FROM_SHORT_HASH, TO_SHORT_HASH = NODES_SHORT_HASH[FROM_COL], NODES_SHORT_HASH[TO_COL]
    # 固定为64的原因主要还是考虑后续会映射到edge dict中, 统一使用64bin去切割
    FROM_SHORT_HASH, TO_SHORT_HASH = 64, 64
    splitfile = SplitFile(*splitfile_arguments)
    os.makedirs(output, exist_ok=True)
    # 随机块大小是为了让进程吃资源的节奏错开
    random_chunk_size = lambda : random.randint(300000, 600000)
    # 针对非高频节点使用使用短hash映射到共享空间，需要独立重排
    from_node_lists = [ArrayList("%s/hid_%d_%s.idxarr.chunk_%d" % \
                        (output, i, FROM_COL, chunk_id), 
                        chunk_size=random_chunk_size(),
                      dtype=[('from', np.int64), ('to', np.int64)]) 
              for i in range(FROM_SHORT_HASH)]
    to_node_lists = [ArrayList("%s/hid_%d_%s.idxarr.chunk_%d" % \
                        (output, i, TO_COL, chunk_id), 
                        chunk_size=random_chunk_size(),
                      dtype=[('from', np.int64), ('to', np.int64)]) 
              for i in range(TO_SHORT_HASH)]
    # 针对高频节点， 使用独立的空间， 不需要重排
    freq_output = f"{output}/freq_edges"
    os.makedirs(freq_output, exist_ok=True)
    ffdict_able_flag, tfdict_able_flag = False, False
    if FROM_COL in freq_nodes: 
        from_node_freq_dict = {fk:ArrayList("%s/hid_%s_%s.idxarr.chunk_%d" % \
                            (freq_output, str(fk), FROM_COL, chunk_id), 
                               chunk_size=random_chunk_size(),
                          dtype=[('from', np.int64), ('to', np.int64)]) 
                  for fk in list(freq_nodes[FROM_COL])}
        from_node_freq_dict_set = set(from_node_freq_dict.keys())
        ffdict_able_flag = True
    if TO_COL in freq_nodes:
        to_node_freq_dict = {tk:ArrayList("%s/hid_%s_%s.idxarr.chunk_%d" % \
                            (freq_output, str(tk), TO_COL, chunk_id), 
                               chunk_size=random_chunk_size(),
                          dtype=[('from', np.int64), ('to', np.int64)]) 
                  for tk in list(freq_nodes[TO_COL])}
        to_node_freq_dict_set = set(to_node_freq_dict.keys())
        tfdict_able_flag = True
    FROM_NODE_TYPE_INDEX, TO_NODE_TYPE_INDEX = 1, 2;
    for line in splitfile:
        # from_str, to_str
        r = line[:-1].split(",")
        if len(r) != 2:
            continue
        h1, h2 = hash(r[0]) << 4 | FROM_NODE_TYPE_INDEX, hash(r[1]) << 4 | TO_NODE_TYPE_INDEX
        # 记录高频节点
        if ffdict_able_flag and (h1 in from_node_freq_dict_set):
            from_node_freq_dict[h1].append((h1, h2))
        else: # 记录非高频节点
            from_node_lists[h1 % FROM_SHORT_HASH].append((h1, h2))
            
        if tfdict_able_flag and (h2 in to_node_freq_dict_set):
            to_node_freq_dict[h2].append((h2, h1))
        else:
            to_node_lists[h2 % TO_SHORT_HASH].append((h2, h1))
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

def unique_inplace(arr, order=None, axis=0, kind='mergesort'):
    # memmap sort inplaced then unique index & counts return
    arr.sort(order=order, axis=axis, kind=kind)
    return np.unique(arr[order], return_index=True, return_counts=True)

import glob
def hid_idx_dict(graph, _id):
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
    # freq部分实际上是被重复写入到dict了
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
    order_idx_pointer = {}
    @staticmethod
    def merge_idx_to(k, ipts):
        '''
        '''
        mems = [np.memmap(f, mode='r', dtype=[('from', np.int64), ('to', np.int64)]) 
                for f in ipts]
        arr = merge_mem_array(mems)
        _val, _idx, _len = unique_inplace(arr, order='from')
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
        
        MergeIndex.toarrconcat[MergeIndex.edge_to_cursor: MergeIndex.edge_to_cursor + arr.shape[0]] = arr['to']
        MergeIndex.edge_to_cursor += arr.shape[0]

    @staticmethod
    def merge_order_idx_to(k, ipts):
        mems = [np.memmap(f, mode='r', dtype=[('from', np.int64), ('to', np.int64)]) 
                for f in ipts]
        return k, mems
        pass

    @staticmethod
    def merge_order_idx_to_callback(args):
        k, mems = args
        value = k
        index = MergeIndex.edge_to_cursor
        length = sum([m.shape[0] for m in mems])
        MergeIndex.order_idx_pointer[value] = (index, length)
        for m in mems:
            MergeIndex.toarrconcat[MergeIndex.edge_to_cursor: MergeIndex.edge_to_cursor + m.shape[0]] = m['to']
            MergeIndex.edge_to_cursor += m.shape[0]
        pass

    @staticmethod
    def order_idx_pointer_dump(graph):
        idxarr = np.memmap(f"{graph}/edges_sort/hid_freq.idx.arr", 
            mode='w+',
            order='F',
            shape=(len(MergeIndex.order_idx_pointer), ), 
            dtype=[('value', np.int64), 
                    ('index', np.int64), 
                    ('length', np.int32)])

        for idx, (value, (index, length)) in enumerate(MergeIndex.order_idx_pointer.items()):
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

    edges_count_sum = sum([np.memmap(f, mode='r', dtype=[('from', np.int64), ('to', np.int64)]).shape[0] 
                for f in sum(list(files_hash_dict.values()) + 
                            list(files_freq_dict.values()), [])])

    os.makedirs(f"{graph}/edges_sort", exist_ok=True)
    MergeIndex.edge_to_cursor = 0
    MergeIndex.toarrconcat = np.memmap(f"{graph}/edges_sort/concat.to.arr", 
            mode='w+',
            shape=(edges_count_sum, ), 
            dtype=[('value', np.int64)])

    pool = Pool(processes=cpu_count())
    stime = time.time()
    for items in list(files_hash_dict.items()):
        pool.apply_async(MergeIndex.merge_idx_to, 
            args=items, 
            callback=MergeIndex.merge_idx_to_callback)
    for items in list(files_freq_dict.items()):
        pool.apply_async(MergeIndex.merge_order_idx_to,
            args=items,
            callback=MergeIndex.merge_order_idx_to_callback)
    pool.close()
    pool.join()
    MergeIndex.order_idx_pointer_dump(graph)
    print(time.time() - stime)



class HashSplitDict():
    def __init__(self, path, dtype=np.int32, hlen=64):
        self.dtype = dtype
        self.hlen = hlen
        self.hdict = self._load(path)
    
    def _load(self, path):
        r = {}
        for i in range(self.hlen):
            r[i] = ArrayDict(memmap_path=f"{path}/hid_%d.dict.arr" % i, 
                  memmap=True,
                  value_dtype=self.dtype, 
                  memmap_mode='r')
        return r
        
    def __setitem__(self, key, value):
        _id = key % self.hlen
        for i in np.unique(_id):
            idx = (_id == i)
            self.hdict[i][key[idx]] = value[idx]
        pass
    
    def __getitem__(self, key):
        ret = np.zeros_like(key, dtype=self.dtype)
        _id = key % self.hlen
        for i in np.unique(_id):
            idx = (_id == i)
            ret[idx] = self.hdict[i][key[idx]]
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
    idx = mapper[seeds]
    idx = idx[idx['length'] > 0]
    def sample_range(_from, _len, neibor_cnt):
        if _len > neibor_cnt:
            return np.random.randint(_from, _from + _len, neibor_cnt)
        else:
            return np.arange(_from, _from + _len)
    R = [sample_range(_f,  _l, neibor)
                        for _f, _l in idx]
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
# import h5py
def test(a, seed):
    global toarrconcat
    global hsd
    bs = graph_sampler(seed, int(sys.argv[3]), int(sys.argv[4]), toarrconcat, hsd)
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
    print("T1:", time.time())
    dataset, graph = sys.argv[1], sys.argv[2]
    print(f"Dataset: {dataset}\nGraph: {graph}")
    print("Relationship Transforming...")
    relationship2indexarray(dataset, graph)
    print(f"Index resorted to edge mergeing...")
    merge_index_array_then_sort(graph)
    print(f"Graph index merge by hashid...")
    hid_idx_merge(graph)
    print("Merge success")
    toarrconcat = np.memmap(f"{graph}/edges_sort/concat.to.arr", 
        mode='r',
        dtype=[('value', np.int64)])['value']
    
    hsd = HashSplitDict(f"{graph}/edges_mapper", 
                    dtype=[('index', np.int64), 
                           ('length', np.int32)], 
                    hlen=64)
    print("T2:", time.time())
    if False:
#         seed = toarrconcat[np.random.randint(0, toarrconcat.shape[0], int(sys.argv[5]))]
        print(time.time())
        stime = time.time()

        pool = Pool(processes=cpu_count())
        res = pool.starmap(test, [(_, toarrconcat[np.random.randint(0, toarrconcat.shape[0], int(sys.argv[5]))]) for _ in range(20)])
        pool.close()
        pool.join()
        print(sample_length, sampler_length)
        print(time.time() - stime)
        print([[b.shape for b in bs] for bs in res])
        
        
    pass
    


if __name__ == "__main__":
    main()



