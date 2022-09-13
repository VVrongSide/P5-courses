import logging
import threading
import time

def increment():
    global C
    C = C+1

def thread_task():
    for _ in range(100000):
        increment()

def main_task():
    global C
    C = 0
    t1 = threading.Thread(target=thread_task)
    t2 = threading.Thread(target=thread_task)
    t1.start()
    t2.start()

if __name__ == "__main__":
    for i in range(10):
        main_task()
        print("Iteration {0}: C = {1}".format(i,C))
