import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from cryptography.fernet import Fernet


"""
############################################################################################
############################################################################################
"""

class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('Encrypted chat')

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
        if self.username == "admin" and entered_password=="test":
            """
            ######
            Connects to the server with a socket and verify that the username is unique.
            ######
            """
            self.label_error.config(text="User is created!", fg="#211A52")
            self.destroy()
            tab = TabGUI()
            tab.mainloop()
            
        else:
            self.label_error.config(text="Invalied username and/or password!", fg="red")


    def __log_in(self):
        entered_username = self.entry_username.get()
        entered_password = self.entry_password.get()
        if entered_username == "admin2" and entered_password=="test2":
            self.label_error.config(text="Login successful!", fg="#211A52")
            """
            ######
            Connects to the server with a socket and verify that the user exist in the database.
            ######
            """
        else:
            self.label_error.config(text="Invalied username and/or password!", fg="red")

"""
############################################################################################
############################################################################################
"""

class TabGUI(MainGUI, tk.Tk):
    def __init__(self):
        super().__init__()
        #self.rootTab = tk.Tk()
        self.geometry('800x600')
        self.title('Encrypted chat')
        self.notebook = ttk.Notebook(self)
        self.default_tab = self.add_default_tab()
        
    def add_default_tab(self):
        self.default = ttk.Frame()
        self.notebook.add(self.default,text="+")
        
        frame1 = ttk.Frame()
        
            # Error message
        label_error = tk.Label(frame1, text=' ')
        label_error.grid(row=0,column=0,columnspan=2)

            # Invitation code label
        label_invite_code = tk.Label(frame1, text='Invitation Code')
        label_invite_code.grid(row=1, column=0, columnspan=2)

            # Text field
        entry_invite_code = tk.Entry(frame1, show='*')
        entry_invite_code.grid(row=2, column=0,columnspan=2)

            # Join chat button
        join_chat = tk.Button(frame1, text='Join Chat',width=13,command=lambda: self.__create_chat_tab(entry_invite_code.get()))
        join_chat.grid(row=3, column=0, padx=15, pady=20)

            # Create chat button
        create_chat = tk.Button(frame1, text='Create Chat',width=13,command=lambda: self.__create_chat_tab(entry_invite_code.get()))
        create_chat.grid(row=3, column=1, padx=15)

        frame1.place(relx=0.5, rely=0.3, anchor=tk.N)


        self.notebook.pack(fill=tk.BOTH, expand=True)



    def __create_chat_tab(self,name):
        
        if name == "admin":  #! Verify name in database  
            
            # Generate encryption key and store it on client side 
            key = Fernet.generate_key()
            f = open(f"{name}_key.txt", "wb")
            f.write(key)
            f.close()

            frame = ttk.Frame()

            # Frame 0 - Text history window
            text_field = ScrolledText(frame, state=tk.DISABLED)
            text_field.pack(fill=tk.BOTH)
            
            # Frame 1 - Input text field
            self.entry_chat_msg = tk.Entry(frame)
            self.entry_chat_msg.pack(side=tk.LEFT, ipadx=230, ipady=20)
            
            # Frame 2 - Send button
            button_send_msg = tk.Button(frame, text='Send',width=10, command=lambda: self.__send_msg(self.entry_chat_msg.get(), key))
            button_send_msg.pack(side=tk.LEFT, expand=1)

            frame.pack()

            self.notebook.insert(0, frame, text=name)
        else:
            print("ERROR")
    

    def __send_msg(self,text_msg, key):
        print(self.username)
        # Encrypt a message
        encryption = Fernet(key)
        secret_msg = encryption.encrypt(bytes(text_msg,'utf-8'))
        print("PT: ", text_msg)
        print("CT: ", secret_msg)
        self.entry_chat_msg.delete(0,'end')
    
        # Decrypt a message
        decryption = Fernet(key)
        print(decryption.decrypt(secret_msg))
        








if __name__=="__main__":

    main = MainGUI()
    main.mainloop()

    #tab = TabGUI()
    #tab.mainloop()
