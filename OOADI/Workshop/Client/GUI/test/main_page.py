
# Libraries to import
import tkinter as tk
from tkinter import ttk

"""
############################################################################################
############################################################################################
"""


class DefaultGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Encrypted chat')        # Title of window
        self.geometry('800x600')            # Window size        
        self.resizable(0,0)                 # Window is not resizable and both x and y directions.
        self.color = '#aed6f1'              # Color 
        self.configure(bg=self.color)       # Set background color
        self.headline_font = ("FreeSans", 16)
        self.error_font = ("FreeSans", 14)
        self.tabControl = ttk.Notebook()   


"""
############################################################################################
############################################################################################
"""

class MainGui(DefaultGUI):
    def __init__(self):
        super().__init__()

        # Frame 0 - Picture
        self.frame = tk.Frame(bg=self.color)
        self.photo = tk.PhotoImage(file='index.png')
        self.image = tk.Label(self.frame, image=self.photo)
        self.image.grid(row=0,column=0,columnspan=2,pady=20)
        self.frame.pack(pady=20)

        # Frame 1 - Error prompt
        self.frame1 = tk.Frame(bg=self.color)

        self.label_error = tk.Label(self.frame1, text=' ',bg=self.color, font=self.error_font)
        self.label_error.grid(row=1,column=0,columnspan=2)

        self.frame1.pack()

        # Frame 2 - Username title and textfield
        self.frame2 = tk.Frame(bg=self.color)
            # Username title
        self.label_username = tk.Label(self.frame2, text='Username',bg=self.color,font=self.headline_font)
        self.label_username.grid(row=2, column=0,columnspan=2, sticky=tk.W)
            # Text field for username
        self.entry_username = tk.Entry(self.frame2)
        self.entry_username.grid(row=3, column=0,columnspan=2)

        self.frame2.pack(pady=10)
        
        
        # Frame 3 - Password title and textfield
        self.frame3 = tk.Frame(bg=self.color)
            # Password title
        self.label_password = tk.Label(self.frame3, text='Password',bg=self.color,font=self.headline_font)
        self.label_password.grid(row=4, column=0,columnspan=2, sticky=tk.W)
            # text field for password 
        self.entry_password = tk.Entry(self.frame3, show='*')
        self.entry_password.grid(row=5, column=0,columnspan=2)

        self.frame3.pack()
        

        # Frame 4 - The two buttons
        self.frame4 = tk.Frame(bg=self.color)
            # Login button
        self.button_login = tk.Button(self.frame4, text='Log-in',font=self.headline_font,width=13, command=lambda: self.__log_in())
        self.button_login.grid(row=6, column=0, padx=15)
            # Create account button
        self.button_create = tk.Button(self.frame4, text='Create account',font=self.headline_font,width=13,command=lambda: self.__create_account())
        self.button_create.grid(row=6, column=1,padx=15)

        self.frame4.pack(pady=35)  

    def __create_account(self):
        entered_username = self.entry_username.get()
        entered_password = self.entry_password.get()
        if entered_username == "admin" and entered_password=="test":
            """
            ######
            Connects to the server with a socket and verify that the username is unique.
            ######
            """
            self.label_error.config(text="User is created!", fg="#211A52")
            self.destroy()
            test = NoChatGUI()
            test.Toplevel()
            
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
class NoChatGUI(DefaultGUI,tk.Tk):
    def __init__(self):
        super().__init__()

        # Create tab
        self.default_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.default_tab, text='+')
        self.tabControl.pack(expand=1, fill=tk.BOTH)
        
        # Frame 1 - Error prompt
        self.frame1 = tk.Frame(bg=self.color)
        
            # Error message
        self.label_error = tk.Label(self.frame1, text=' ',bg=self.color, font=self.error_font)
        self.label_error.grid(row=0,column=0,columnspan=2)

            # Invitation code label
        self.label_invite_code = tk.Label(self.frame1, text='Invitation Code',bg=self.color,font=self.headline_font)
        self.label_invite_code.grid(row=1, column=0, columnspan=2)

            # Text field
        self.entry_invite_code = tk.Entry(self.frame1, show='*')
        self.entry_invite_code.grid(row=2, column=0,columnspan=2)

            # Join chat button
        self.join_chat = tk.Button(self.frame1, text='Join Chat',font=self.headline_font,width=13, command=lambda: self.__join_chat())
        self.join_chat.grid(row=3, column=0, padx=15, pady=20)

            # Create chat button
        self.create_chat = tk.Button(self.frame1, text='Create Chat',font=self.headline_font,width=13, command=lambda: self.__create_chat())
        self.create_chat.grid(row=3, column=1, padx=15)

        self.frame1.place(relx=0.5, rely=0.4, anchor=tk.N)
        
    def __join_chat(self):
        entered_invite_code = self.entry_invite_code.get()
        print(entered_invite_code)
        if entered_invite_code == 'Connie':
            self.label_error.config(text="You entered Connie!", fg="#211A52")
            """
            ######
            Connects to the server with a socket and verify that the invitation code exist.
            Make P2P to get the encryption key.
            ######
            """
        else:
            self.label_error.config(text="Invalied invitation code", fg="red")


    def __create_chat(self):
        entered_invite_code = self.entry_invite_code.get()
        print(entered_invite_code)
        if entered_invite_code == 'Connie':
            self.label_error.config(text="New chat of Connie! is ready", fg="#211A52")
            """
            ######
            Verify the invitation code is unique and create encryption key.
            ######
            """
            self.tabControl.insert(self.default_tab, text=entered_invite_code)
            self.tabControl.select(self.default_tab)
            
        else:
            self.label_error.config(text="Invalied invitation code", fg="red")

"""
############################################################################################
############################################################################################
"""

class ChatGUI(DefaultGUI):
    def __init__(self, name):
        super().__init__()
        self.chat_name = name        
        
        # Create chat window tab
        self.chat_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.chat_tab, text=self.chat_name)
        self.tabControl.pack(expand=1, fill=tk.BOTH)

        # Frame 0 - Text history window
        self.text_field = ScrolledText(self.chat_tab, state=tk.DISABLED)
        self.text_field.pack(fill=tk.BOTH)

        # Frame 1 - Input text field
        self.chat_message = tk.Entry(self.chat_tab)
        self.chat_message.pack(side=tk.LEFT, ipadx=230, ipady=20)

        # Frame 2 - Send button
        self.send_button = tk.Button(self.chat_tab, text='Send',font=self.headline_font,width=10, command=lambda: self.__send_msg())
        self.send_button.pack(side=tk.LEFT, expand=1)

        rx_thread = threading.Thread(target=self.__receive_msg())
        rx_thread.start()

    def __send_msg(self):
        msg = self.chat_message.get()   # Get string from input text field.
        """
        ######
        Encode message and send over socket to the server.
        ######
        """
        
        
        print(msg)
        self.chat_message.delete(0,'end')   # Delete string in input text field.

    def __receive_msg(self):
        
        while True:
            time.sleep(5)
            with open("text.txt", "r") as f:
                for x in f:
                    print(x)
            """
            ######
            Create thread to receive messages from server and insert them to history chat.
            ######
            """
        


if __name__=="__main__":
    test = MainGui()
    test.mainloop()