from threading import *
import time

s=Semaphore(2)

def wish(name):
    for i in range(3):
        s.acquire()
        print("Executing {}".format(name))
        time.sleep(2)
        s.release()

t1=Thread(target=wish, args=("Thread 1",))
t2=Thread(target=wish, args=("Thread 2",))
t3=Thread(target=wish, args=("Thread 3",))
t4=Thread(target=wish, args=("Thread 4",))
t5=Thread(target=wish, args=("Thread 5",))
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
