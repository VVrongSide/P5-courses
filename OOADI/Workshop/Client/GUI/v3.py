from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading
import queue

# Extra
import time


class TabGUI(Tk):
    def __init__(self):
        super().__init__()
        #self.rootTab = tk.Tk()
        self.geometry('800x600')
        self.title('Encrypted chat')
        self.notebook = ttk.Notebook(self)
        self.default_tab = self.add_default_tab()
        self.channel_names = ['comtek2022','Secret']
        self.tab_names = {}
    
    def run(self):
        if len(self.channel_names) != 0:
            for name in self.channel_names:
                chat = Channel(self, name)
                chat.create_chat_tab()
                tab_names = [self.notebook.tab(i, option="text") for i in self.notebook.tabs()]
                self.tab_names[tab_names[0]] = chat
                 
        time.sleep(2)
        t1 = threading.Thread(target=self.__recieve_msg)
        t1.start()
        print(self.tab_names)
        

    def add_default_tab(self):
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
        if invite_code == 'comtek':
            confirmation = True
        #! ###################################
        if confirmation == True:
            self.__create_chat_tab(invite_code)
            self.label_error.config(text="Succes!", fg="blue")
        else:
            self.label_error.config(text="Something went wrong, try again!", fg="red")

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

    def __recieve_msg(self):


        time.sleep(2)

        for index in update:
            if index[0] in self.tab_names.keys():
                tab_object = self.tab_names.get(index[0])
                tab_object.update_channel(index[1])

        time.sleep(2)

        for index in update2:
            if index[0] in self.tab_names.keys():
                tab_object = self.tab_names.get(index[0])
                tab_object.update_channel(index[1])



class Channel(Frame):
    def __init__(self, parent, name):
        Frame.__init__(self)
        self.parent = parent
        self.name = name
        #self.log = log

    def create_chat_tab(self):   
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
        self.text_field.config(state=NORMAL)
        self.text_field.delete('0.0', END)
        line_num = float(1.0)    
        for post in channel_log:
            post_entry = post[0]+ ' - ' + post[1]+': '+ post[2] + '\n'
            self.text_field.insert(str(line_num),post_entry)
            line_num = line_num + 1
        


if __name__=="__main__":

  
    C = ['Secret',[['07-11-2022 16:59', 'Anonymous', 'Its a secret!! Dont tell..']]]
    A = ['comtek2022',[['25-08-22 14:20','Faur','Hvem ved hvad klokken er ??'],['25-08-22 14:23','Pure Genie','14:27 why ??'],['25-08-22 14:24','Wrongside','Mads?'],['25-08-22 14:26','SnooGiraffe','Bajer!!!!']]]
    update = [C,A]

    B = ['Secret',[['07-11-2022 16:59', 'Anonymous', 'Its a secret!! Dont tell..'],['07-11-2022 17:00', 'CIA', 'Dont mind, I already KNOW!! ;)']]]
    update2 = [B,A]

    
    main = TabGUI()
    main.run()
    main.mainloop()