import  threading
from queue import Queue
import time
import copy


def job(l, q):
    res = sum(l)
    q.put(res)


def multithreading(l):
    q = Queue()
    threads = []
    for i in range(4):
        t = threading.Thread(target=job, args=(copy.copy(l), q), name='T%i' %i)
        t.start()
        threads.append(t)

    for thread in threads:
        t.join()
    total = 0
    for _ in range(4):
        total += q.get()
    print(total)

def normal(l):
    total = sum(l)
    print(total)

if __name__ == '__main__':
    l = list(range(1000000))
    s_t = time.time()
    normal(l*4)
    print('normal: ', time.time() - s_t)
    s_t = time.time()
    multithreading(l)
    print('multithreading: ', time.time() - s_t)