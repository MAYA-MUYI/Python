import threading
import time
from queue import Queue


def job(l, q):
    for i in range(len(l)):
        l[i] = l[i]**2
    q.put(l) #将数据推送到队列，多线程不支持返回值


def main():

    q = Queue()
    threads = []
    results = []
    data = [[1, 2, 3], [3, 4, 5], [4, 4, 4], [5, 5, 5]]
    for i in range(4):
        t = threading.Thread(target=job, args=(data[i], q)) #创建线程，可用args传入参数，记得传入队列
        t.start()
        threads.append(t)   #将每个线程加入到线程列表
    for thread in threads:
        thread.join()   #将线程加入到主线程

    for _ in range(4):
        results.append(q.get()) #获取队列里面的列表数据
    print(results)

if __name__ == '__main__':
    main()