
# Libraries to import
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading
from sessionManager import UI_Session_Manager as USM
from sessionManager import UI_Channel_Manager as UCM
import socket

# Only for testing
import time

"""
############################################################################################
############################################################################################
"""

class MainGUI(Tk):
    """Main window of the encrypted chat program. 
    This class creates the GUI, handles user credentials the server.     
    """
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('Encrypted chat')
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.USM = USM(self.socket)
        # Frame 0 - Picture
        self.frame = Frame()
        self.photo = PhotoImage(file='index.png')
        self.image = Label(self.frame, image=self.photo)
        self.image.grid(row=0,column=0,columnspan=2,pady=20)
        self.frame.pack(pady=20)
        # Frame 1 - Error prompt
        self.frame1 = Frame()
        self.label_error = Label(self.frame1, text=' ')
        self.label_error.grid(row=1,column=0,columnspan=2)
        self.frame1.pack()
        # Frame 2 - Username title and textfield
        self.frame2 = Frame()
            # Username title
        self.label_username = Label(self.frame2, text='Username')
        self.label_username.grid(row=2, column=0,columnspan=2, sticky=W)
            # Text field for username
        self.entry_username = Entry(self.frame2)
        self.entry_username.grid(row=3, column=0,columnspan=2)
        self.entry_username.focus()
        self.frame2.pack(pady=10)
        # Frame 3 - Password title and textfield
        self.frame3 = Frame()
            # Password title
        self.label_password = Label(self.frame3, text='Password')
        self.label_password.grid(row=4, column=0,columnspan=2, sticky=W)
            # Text field for password 
        self.entry_password = Entry(self.frame3, show='*')
        self.entry_password.grid(row=5, column=0,columnspan=2)
        self.frame3.pack()
        # Frame 4 - The two buttons
        self.frame4 = Frame()
            # Login button
        self.button_login = Button(self.frame4, text='Log-in',width=13, command=lambda: self.__log_in())
        self.button_login.grid(row=6, column=0, padx=15)
            # Create account button
        self.button_create = Button(self.frame4, text='Create account',width=13,command=lambda: self.__create_account())
        self.button_create.grid(row=6, column=1,padx=15)
        self.frame4.pack(pady=35) 


    def __create_account(self):
        """Verifiy the user credentials is unique on the server-side.

        Return:
            If True: Close main window and opens a new window to manage all chats.
            If False: Make an error prompt in the main window. 
        """   
        
        self.username = self.entry_username.get()
        entered_password = self.entry_password.get()
        
        check = self.USM.createUser(self.username, entered_password)
            
        if check:
            self.destroy()
            tab = TabGUI(self.USM)
            tab.run()
            tab.mainloop() 
        else:                                                           
            self.label_error.config(text="Invalied username and/or password!", fg="red")


    def __log_in(self):  
        """Verifiy the user credentials exsit on the server database.

        Return:
            If True: Close main window and opens a new window to manage all the channels.
            If False: Make an error prompt in the main window. 
        """
        self.username = self.entry_username.get()
        entered_password = self.entry_password.get()


        check, channels = self.USM.login(self.username, entered_password)
        #! Create a socket connection to the server.
        #! Verify in the database that the username and password is valid.
        #! Returns a boolean regarding the result and a list with chats.

        if check:
        #!  #####################################
            self.destroy()
            tab = TabGUI(self.USM, channels)  # Instance of TabGUI class
            tab.run()       #! Pass list of channels here.
            tab.mainloop()  # Makes the GUI visible
        else:                                                        
            self.label_error.config(text="Invalied username and/or password!", fg="red")

"""
############################################################################################
############################################################################################
"""

class TabGUI(Tk):
    """Window with tabs to manage new and existing chats.  
    This class has a default tab at all time to create and join channels. 
    A tab bar provides the option to switch between the different channels.    
    """
    def __init__(self, SM, channels=[]):
        super().__init__()
        #self.rootTab = tk.Tk()
        self.SM = SM
        self.geometry('800x600')
        self.title('Encrypted chat')
        self.notebook = ttk.Notebook(self)
        self.default_tab = self.add_default_tab()
        self.channel_names = channels
        self.tab_names = {}
    
    def run(self):
        """Initialize a channel tab for every channel the user is a part of. 
        Starts a background thread which waits for server updates any connected channels. 
        """
        if len(self.channel_names) != 0:            # Verify if the user is part of any chats.
            for name in self.channel_names:         # Iterate the list
                chat = Channel(self, name)          # Create a Channel intance for every chat
                chat.create_chat_tab()              # Fill the Channel intance with the chat
                tab_names = [self.notebook.tab(i, option="text") for i in self.notebook.tabs()]     # Retieves the names of all tabs.
                self.tab_names[tab_names[0]] = chat # Connects a tab name to a Channel intance in a dictionaries
                 
        time.sleep(1)
        t1 = threading.Thread(target=self.__recieve_msg)
        t1.start()
        

    def add_default_tab(self):
        """Create the default tab for the channel manager window.
        Offers the option to join or create channels.
        """
        self.default = ttk.Frame()
        self.notebook.add(self.default,text="+")
        
        self.frame1 = ttk.Frame()
            # Error message
        self.label_error = Label(self.frame1, text=' ')
        self.label_error.grid(row=0,column=0,columnspan=2)
            # Invitation code label
        self.label_invite_code = Label(self.frame1, text='Invitation Code')
        self.label_invite_code.grid(row=1, column=0, columnspan=2)
            # Text field
        self.entry_invite_code = Entry(self.frame1, show='*')
        self.entry_invite_code.grid(row=2, column=0,columnspan=2)
        self.entry_invite_code.focus()
            # Join chat button
        self.join_chat = Button(self.frame1, text='Join Chat',width=13,command=lambda: self.__join_chat_button(self.entry_invite_code.get()))
        self.join_chat.grid(row=3, column=0, padx=15, pady=20)
            # Create chat button
        self.create_chat = Button(self.frame1, text='Create Chat',width=13,command=lambda: self.__create_chat_button(self.entry_invite_code.get()))
        self.create_chat.grid(row=3, column=1, padx=15)
        self.frame1.place(relx=0.5, rely=0.3, anchor=N)
        self.notebook.pack(fill=BOTH, expand=True)


    def __join_chat_button(self, invite_code):
        """Request to join an exsiting channel with the invitation code.

        Args:
            invite_code (string): invitation code and the name of the channel.
        Return:
            Accepted: Creates a new channel tab.
            Denied: Error prompt
        """      
        self.entry_invite_code.delete(0, 'end')        
        #! Verify invite_code is in database. 
        #! Get encryption token from another user.
        #! Get channel log from database.
        confirmation = False
        if invite_code == 'comtek2020':
            confirmation = True
        #! ##################################
        if confirmation == True:
            chat = Channel(self, invite_code)  
            chat.create_chat_tab()
            tab_names = [self.notebook.tab(i, option="text") for i in self.notebook.tabs()]     
            self.tab_names[tab_names[0]] = chat
            self.label_error.config(text="Succes!", fg="blue")
        else:
            self.label_error.config(text="Invalied invitation code!", fg="red")

  
    def __create_chat_button(self, invite_code):
        """Request to create a new channel with the name of the invitation code.

        Args:
            invite_code (string):
        Return:
            Accepted: Create a new tab for the channel.
            Denied: Error prompt in default tab.
        """
        self.entry_invite_code.delete(0, 'end')        
        #! Verify invite_code's uniqueness in database.
        #! Create encryption token and store locally.

        #! ###################################
        if self.SM.createChannel(invite_code):
            chat = Channel(self, invite_code)  
            chat.create_chat_tab()
            tab_names = [self.notebook.tab(i, option="text") for i in self.notebook.tabs()]     
            self.tab_names[tab_names[0]] = chat
            self.label_error.config(text="Succes!", fg="blue")
        else:
            self.label_error.config(text="Something went wrong, try again!", fg="red")


    def __send_button(self, msg):
        """Encrypts the message and passes it on for transmission 

        Args:
            msg (string): 
        """
        #! Encrypt the message.
        ct_msg = msg 
        #! ###########################
        t = threading.Thread(target=self.__send_msg(msg))
        t.start()
        self.entry_chat_msg.delete(0, 'end')


    def __send_msg(self, CT_msg):
        """Connects and forward the encrypted message to the server.

        Args:
            CT_msg (string): Encrypted message 
        """
        while True:
            #! Need socket object
            #! #######################
            message = CT_msg
            SOCKET_OBJECT.send(message)
            break


    def __recieve_msg(self):
        """Waits for the server to send update to any channel.
        Upon recieving some data a request to update a tab channel is made.
        """
        #! Need socket object
        #! #######################      
        time.sleep(2)
        #! #######################      
        # for index in update:
        #     if index[0] in self.tab_names.keys():
        #         tab_object = self.tab_names.get(index[0])
        #         tab_object.update_channel(index[1])
        # time.sleep(2)
        # for index in update2:
        #     if index[0] in self.tab_names.keys():
        #         tab_object = self.tab_names.get(index[0])
        #         tab_object.update_channel(index[1])

"""
############################################################################################
############################################################################################
"""

class Channel(Frame):
    """Channel class used to create channel tabs.

    Args:
        Frame (object): Tkinter frame object
    """
    def __init__(self, parent, name):
        Frame.__init__(self)
        self.parent = parent
        self.name = name


    def create_chat_tab(self):
        """Fill the tab with a channel log text field and a text input field.
        """   
        self.frame = ttk.Frame()
        # Frame 0 - Text history window
        self.text_field = ScrolledText(self.frame, state=DISABLED)
        self.text_field.pack(fill=BOTH)
        # Frame 1 - Input text field
        self.entry_chat_msg = Entry(self.frame)
        self.entry_chat_msg.pack(side=LEFT, ipadx=230, ipady=20)
        self.entry_chat_msg.focus()
        # Frame 2 - Send button
        self.button_send_msg = Button(self.frame, text='Send',width=10, command=lambda: self.__send_button(self.entry_chat_msg.get()))
        self.button_send_msg.pack(side=LEFT, expand=1)
        self.frame.pack()
        self.parent.notebook.insert(0, self.frame, text=self.name)


    def update_channel(self, channel_log):
        """Update an the channel log text field in an exsiting channel.
        """
        self.text_field.config(state=NORMAL)
        self.text_field.delete('0.0', END)
        line_num = float(1.0)    
        for post in channel_log:
            post_entry = post[0]+ ' - ' + post[1]+': '+ post[2] + '\n'
            self.text_field.insert(str(line_num),post_entry)
            line_num = line_num + 1        
"""
############################################################################################
############################################################################################
"""


if __name__=="__main__":
    C = ['Secret',[['07-11-2022 16:59', 'Anonymous', 'Its a secret!! Dont tell..']]]
    A = ['comtek2022',[['25-08-22 14:20','Faur','Hvem ved hvad klokken er ??'],['25-08-22 14:23','Pure Genie','14:27 why ??'],['25-08-22 14:24','Wrongside','Mads?'],['25-08-22 14:26','SnooGiraffe','Bajer!!!!']]]
    update = [C,A]
    B = ['Secret',[['07-11-2022 16:59', 'Anonymous', 'Its a secret!! Dont tell..'],['07-11-2022 17:00', 'CIA', 'Dont mind, I already KNOW!! ;)']]]
    # update2 = [B,A]

    main = MainGUI()
    main.mainloop()