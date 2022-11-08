

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import os



class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('800x600')
        self.root.title('Encrypted chat')
        self.root.resizable(0,0)
        

class MainGUI():
    def __init__(self):
        super().__init__()
        self = GUI()

         # Frame 0 - Picture
        self.frame = tk.Frame()
        self.photo = tk.PhotoImage(file='index.png')
        self.image = tk.Label(self.frame, image=self.photo)
        self.image.grid(row=0,column=0,columnspan=2,pady=20)
        self.frame.pack(pady=20)

        # Frame 1 - Error prompt
        self.frame1 = tk.Frame()

        self.label_error = tk.Label(self.frame1, text=' ')
        self.label_error.grid(row=1,column=0,columnspan=2)

        self.frame1.pack()

        # Frame 2 - Username title and textfield
        self.frame2 = tk.Frame()
            # Username title
        self.label_username = tk.Label(self.frame2, text='Username')
        self.label_username.grid(row=2, column=0,columnspan=2, sticky=tk.W)
            # Text field for username
        self.entry_username = tk.Entry(self.frame2)
        self.entry_username.grid(row=3, column=0,columnspan=2)
        self.entry_username.focus()

        self.frame2.pack(pady=10)
        
        
        # Frame 3 - Password title and textfield
        self.frame3 = tk.Frame()
            # Password title
        self.label_password = tk.Label(self.frame3, text='Password')
        self.label_password.grid(row=4, column=0,columnspan=2, sticky=tk.W)
            # text field for password 
        self.entry_password = tk.Entry(self.frame3, show='*')
        self.entry_password.grid(row=5, column=0,columnspan=2)

        self.frame3.pack()
        

        # Frame 4 - The two buttons
        self.frame4 = tk.Frame()
            # Login button
        self.button_login = tk.Button(self.frame4, text='Log-in',width=13, command=lambda: self.__log_in())
        self.button_login.grid(row=6, column=0, padx=15)
            # Create account button
        self.button_create = tk.Button(self.frame4, text='Create account',width=13,command=lambda: self.__create_account())
        self.button_create.grid(row=6, column=1,padx=15)

        self.frame4.pack(pady=35)


if __name__=="__main__":

    chat_name = 'comtek2020'
    chatlog_comtek = [['25-08-22 14:20','Faur','Hvem ved hvad klokken er ??'],['25-08-22 14:23','Pure Genie','14:27 why ??'],['25-08-22 14:24','Wrongside','Mads?'],['25-08-22 14:26','SnooGiraffe','Bajer!!!!']]


    main = MainGUI()
    main.mainloop()
    
