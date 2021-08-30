from multiprocessing import Process,Queue,Pool
import os

def run_proc(name):
    print('Run child process %s (%s)...' %(name, os.getpid()))

if __name__ == '__main__':
    print('Process process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')

def job(q):
    res=0
    for i in range(1000):
        res+=i+i**2+i**3
    q.put(res)    #queue

if __name__=='__main__':
    q = Queue()
    p1 = Process(target=job,args=(q,))
    p2 = Process(target=job,args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    res1 = q.get()
    res2 = q.get()
    print(res1+res2)