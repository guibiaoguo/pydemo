from multiprocessing import Pool,Process
import threading
import os, time, random

def long_time_task(name,test,test1):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    #b1 = threading.Thread(target=thread_time_task,args=(2,))
    #b1.start()
    #b1.join()
    print('Task %s run %0.2f secode' % (name, (end - start)))

def thread_time_task(name):
    print('Run thread_task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('thread Task %s run %0.2f secode' % (name, (end - start)))

def time_task(name):
    print('Run main task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    for i in range(20):
        print(f"main task {i}")
        time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s run %0.2f secode' % (name, (end - start)))

if __name__ == '__main__':
    request_pro = Process(target=time_task, args=("main",))
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,2,3))
    print('Waiting for all subprocess done...')
    request_pro.start()
    request_pro.join()
    p.close()
    p.join()
    
    print('All subprocess done.')

    