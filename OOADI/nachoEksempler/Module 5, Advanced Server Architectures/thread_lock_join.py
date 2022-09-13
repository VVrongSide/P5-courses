from threading import *
import time

l=Lock()

def wish(name):
    for i in range(3):
        l.acquire()
        print("Executing {}".format(name))
        time.sleep(0.2)
        l.release()

t1=Thread(target=wish, args=("Thread 1",))
t2=Thread(target=wish, args=("Thread 2",))
t1.start()
t2.start()
t1.join()
t2.join()
