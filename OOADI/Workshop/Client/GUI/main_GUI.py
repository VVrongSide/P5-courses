import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading


# Extra
import time

"""
############################################################################################
############################################################################################
"""

class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('Encrypted chat')

        
    def setup(self):
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


    def __create_account(self):     
        self.username = self.entry_username.get()
        entered_password = self.entry_password.get()
        
        #! Create a socket connection to the server.
        #! Verify in the database that the username is unique.
        #! Returns a boolean regarding the result. 
            
        if self.username == "WrongSide" and entered_password=="admin":  
            #! #########################
            self.destroy()
            tab = TabGUI()
            tab.run() 
        else:                                                           
            self.label_error.config(text="Invalied username and/or password!", fg="red")


    def __log_in(self):    
        self.username = self.entry_username.get()
        entered_password = self.entry_password.get()

        #! Create a socket connection to the server.
        #! Verify in the database that the username and password is valid.
        #! Returns a boolean regarding the result. 

        if self.username == "admin" and entered_password=="test":  
            #!  #####################################
            self.destroy()
            tab = TabGUI()
            tab.run()

        else:                                                        
            self.label_error.config(text="Invalied username and/or password!", fg="red")


"""
############################################################################################
############################################################################################
"""

class TabGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.rootTab = tk.Tk()
        self.geometry('800x600')
        self.title('Encrypted chat')
        self.notebook = ttk.Notebook(self)
        self.default_tab = self.add_default_tab()
    
    def run(self):
        t1 = threading.Thread(target=self.__recieve_msg)
        t1.start()


    def add_default_tab(self):
        self.default = ttk.Frame()
        self.notebook.add(self.default,text="+")
        
        self.frame1 = ttk.Frame()
            # Error message
        self.label_error = tk.Label(self.frame1, text=' ')
        self.label_error.grid(row=0,column=0,columnspan=2)
            # Invitation code label
        self.label_invite_code = tk.Label(self.frame1, text='Invitation Code')
        self.label_invite_code.grid(row=1, column=0, columnspan=2)
            # Text field
        self.entry_invite_code = tk.Entry(self.frame1, show='*')
        self.entry_invite_code.grid(row=2, column=0,columnspan=2)
        self.entry_invite_code.focus()
            # Join chat button
        self.join_chat = tk.Button(self.frame1, text='Join Chat',width=13,command=lambda: self.__join_chat_button(self.entry_invite_code.get()))
        self.join_chat.grid(row=3, column=0, padx=15, pady=20)
            # Create chat button
        self.create_chat = tk.Button(self.frame1, text='Create Chat',width=13,command=lambda: self.__create_chat_button(self.entry_invite_code.get()))
        self.create_chat.grid(row=3, column=1, padx=15)
        self.frame1.place(relx=0.5, rely=0.3, anchor=tk.N)
        self.notebook.pack(fill=tk.BOTH, expand=True)


    def __join_chat_button(self, invite_code):      
        self.entry_invite_code.delete(0, 'end')        
        #! Verify invite_code is in database. 
        #! Get encryption token from another user.
        #! Get channel log from database.
        confirmation = False
        if invite_code == 'comtek2020':
            confirmation = True
        #! ##################################
        if confirmation == True:
            self.__create_chat_tab(invite_code)
            self.label_error.config(text="Succes!", fg="blue")
        else:
            self.label_error.config(text="Invalied invitation code!", fg="red")

  
    def __create_chat_button(self, invite_code):
        self.entry_invite_code.delete(0, 'end')        
        #! Verify invite_code's uniqueness in database.
        #! Create encryption token and store locally.
        confirmation = False
        if invite_code == 'hey':
            confirmation = True
        #! ###################################
        if confirmation == True:
            self.__create_chat_tab(invite_code)
            self.label_error.config(text="Succes!", fg="blue")
        else:
            self.label_error.config(text="Something went wrong, try again!", fg="red")


    def __create_chat_tab(self,tab_name):   
        self.frame = ttk.Frame()
        #self.notebook.add(self.frame,text=invite_code)
        # Frame 0 - Text history window
        self.text_field = ScrolledText(self.frame, state=tk.DISABLED)
        self.text_field.pack(fill=tk.BOTH)
        # Frame 1 - Input text field
        self.entry_chat_msg = tk.Entry(self.frame)
        self.entry_chat_msg.pack(side=tk.LEFT, ipadx=230, ipady=20)
        self.entry_chat_msg.focus()
        # Frame 2 - Send button
        self.button_send_msg = tk.Button(self.frame, text='Send',width=10, command=lambda: self.__send_button(self.entry_chat_msg.get()))
        self.button_send_msg.pack(side=tk.LEFT, expand=1)
        self.frame.pack()
        self.notebook.insert(0, self.frame, text=tab_name)
   
    def __recieve_msg(self):
        while True:
            time.sleep(5)
            print('Time is up')
            #! Need socket object
            #message = SOCKET_OBJECT.recv(BUFFER)
            #! #####################################
            

            
            """
            self.text_field.config(state=tk.NORMAL)
            line_num = float(1.0)    
            for post in chatlog_comtek:
                post_entry = post[0]+ ' - ' + post[1]+': '+ post[2] + '\n'
                self.text_field.insert(str(line_num),post_entry)
                line_num = line_num + 1
            """

    def __send_button(self, msg):
        #! Encrypt the message.
        self.CT_msg = msg 
        #! ###########################
        t = threading.Thread(target=self.__send_msg)
        t.start()
        
        self.entry_chat_msg.delete(0, 'end')


    def __send_msg(self):
        while True:
            #! Need socket object
            #! #######################
            message = self.CT_msg
            SOCKET_OBJECT.send(message)
            break

"""
############################################################################################
############################################################################################
"""



if __name__=="__main__":

    update = [['comtek',[['25-08-22 14:20','Faur','Hvem ved hvad klokken er ??'],['25-08-22 14:23','Pure Genie','14:27 why ??'],['25-08-22 14:24','Wrongside','Mads?'],['25-08-22 14:26','SnooGiraffe','Bajer!!!!']]], ['Secret',['07-11-2022', 'Anonymous', 'Its a secret!! Dont tell..']]]

    

    chat_name = 'comtek2020'
    chatlog_comtek = [['25-08-22 14:20','Faur','Hvem ved hvad klokken er ??'],['25-08-22 14:23','Pure Genie','14:27 why ??'],['25-08-22 14:24','Wrongside','Mads?'],['25-08-22 14:26','SnooGiraffe','Bajer!!!!']]

    def main():
        main = MainGUI()
        main.setup()


    t = threading.Thread(target=main)
    t.start()
