from threading import *
import time

def wish(name):
    for i in range(3):
        print("Executing {}".format(name))
        time.sleep(2)

t1=Thread(target=wish, args=("Thread 1",))
t2=Thread(target=wish, args=("Thread 2",))
t1.start()
t2.start()
