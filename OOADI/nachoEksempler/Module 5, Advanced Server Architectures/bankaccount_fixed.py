import threading
from random import randint

l=threading.Lock()

class bankAccount(object):
    def __init__(self, initialmoney = 0):
        self.balance = initialmoney
    def withdraw(self, amount):
        if self.balance <= 0 or self.balance-amount <0:
            print("You do not have that much money\n")
        else:
            self.balance -= amount
            print("Withdrawn {}\n".format(amount))
        self.checkAvailable()
    def deposit(self, amount):
        self.balance += amount
        print("Deposited {}\n".format(amount))
        self.checkAvailable()
    def checkAvailable(self):
        print("Available {}\n".format(self.balance))
class depositThread(threading.Thread):
    def __init__(self,account_name,value):
        threading.Thread.__init__(self)
        self.bankaccount=account_name
        self.amount=value
    def run(self):
        l.acquire()
        self.bankaccount.deposit(self.amount)
        l.release()
        
class withdrawThread(threading.Thread):
    def __init__(self,account_name,value):
        threading.Thread.__init__(self)
        self.bankaccount=account_name
        self.amount=value
    def run(self):
        l.acquire()
        self.bankaccount.withdraw(self.amount)
        l.release()

       
def main():
    account=bankAccount(100)
    print("Bank Account created\n")
    account.checkAvailable()
    t1 = depositThread(account,30)
    t1.start()
    t2 = depositThread(account,20)
    t2.start()
    t3 = depositThread(account,10)
    t3.start()
    t4 = withdrawThread(account,30)
    t4.start()
    t5 = withdrawThread(account,50)
    t5.start()
    t6 = withdrawThread(account,20)
    t6.start()
    account.checkAvailable()
    
# Call the main fucntion only if the file has not been
# imported into another program
if __name__ == "__main__":
    main()
