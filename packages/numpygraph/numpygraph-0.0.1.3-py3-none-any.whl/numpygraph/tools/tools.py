import numpy as np
import os
from functools import lru_cache

import threading
import queue
import threading
import queue
from fileshutil import *
    
# class ThreadFileIterator():
#     '''异步读文件，实际提升不明显
#     '''
#     @staticmethod
#     def thread_read(iterator, queue):
#         BATCH_SIZE = 2000000
#         batch, size = [], 0
#         for l in iterator:
#             batch.append(l)
#             size += 1
#             if size == BATCH_SIZE:
#                 queue.put(batch)
#                 del batch
#                 batch, size = [], 0
#         batch.append("")
#         queue.put(batch)

#     def __init__(self, iterator, maxsize=50):
#         self.queue = queue.Queue(maxsize=maxsize)
#         self.thread = threading.Thread(target=ThreadFileIterator.thread_read, 
#                                        args=(iterator, self.queue,))
#         self.thread.setDaemon(True)
#         self.thread.start()
#         self.thread_iterator = self._thread_iterator()
#         pass
    
#     def __iter__(self):
#         return self
    
#     def _thread_iterator(self):
#         while True:
#             batch = self.queue.get()
#             for l in batch:
#                 if l == "":
#                     return
#                 yield l
        
#     def __next__(self):
#         return next(self.thread_iterator)
            
# class SplitFile():
#     '''分片文件
#     '''
#     @staticmethod
#     def split(path, num, jump=0, dist_random=False):
#         '''dist_random: 文件是否采用随机切割
#         True: 随机切割
#         False: 均匀切割
#         '''
#         f = open(path)
#         for _ in range(jump):
#             f.readline()
#         size = os.path.getsize(path)
#         _froms = [int((i / num) * size) for i in range(num)]
#         _tos = [f.seek(_f) and f.readline() and f.tell() for _f in _froms[1:]] + [None]
#         return [(path, _f, _t) for _f, _t in zip(_froms, _tos)]
    
#     def __init__(self, path, _from, _to):
#         self.f = open(path)
#         self._from = _from
#         self._to = _to
#         self.f.seek(self._from)
#         self.cursor = self.f.tell()
#         self.prev_cursor = self.cursor
#         pass
    
# #     @profile
#     def __iter__(self):
#         return self
    
# #     @profile
#     def __next__(self):
#         l = self.f.readline()
#         if l is '' or ((self._to is not None) and self.cursor > self._to):
#             raise StopIteration
#         self.prev_cursor = self.cursor
#         self.cursor += len(l.encode('utf-8'))
#         return l
    
#     def tell(self):
#         return self.cursor
    
    