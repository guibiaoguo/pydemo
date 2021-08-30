from multiprocessing import Pool,Queue
import os, time, random
from multiprocessing.queues import Empty

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(0.0003)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))
    return name*name

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(2)
    # p.map p.apply_asyn 只能有一个参数
    #for i in range(5):
    #    p.apply_async(long_time_task, args=(i,))
    res=p.map(long_time_task,range(5))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    print(res)