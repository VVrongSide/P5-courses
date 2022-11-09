from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import time
import threading

class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry('800x600')
        self.title('Encrypted chat')
        self.notebook = ttk.Notebook()
        self.initial_window()
        self.run()
        
    def run(self):
        t1 = threading.Thread(target=self.recv)
        t1.start()

    def recv(self):
        
        time.sleep(2)
        update_len = len(update)
        channel = update[0]
        chat = TAB(self, channel[0], channel[1])
        #self.notebook.add(chat, text=channel[0])    
        self.notebook.insert(0, chat, text=channel[0])
            

        """
        for channel in update:
            print(channel[0])
            chat = TAB(channel[0], channel[1])
            
            print(chat)
            self.notebook.insert(0, chat, text=channel[0])
            #chat.update_chat()
        """ 


    def initial_window(self):
        frame = ttk.Frame()
        self.notebook.add(frame,text="+")
        
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



class TAB(ttk.Frame):
    def __init__(self, parent, channel_name, channel_content):
        Frame.__init__(self, parent)
        self.parent = parent
        self.name = channel_name
        self.log = channel_content

    def initial_chat(self):   
        self.frame = ttk.Frame()
        # Frame 0 - Text history window
        self.text_field = ScrolledText(self.frame, state=DISABLED)
        self.text_field.pack(fill=BOTH)
        # Frame 1 - Input text field
        entry_chat_msg = Entry(self.frame)
        entry_chat_msg.pack(side=LEFT, ipadx=230, ipady=20)
        entry_chat_msg.focus()
        # Frame 2 - Send button
        button_send_msg = Button(self.frame, text='Send',width=10, command=lambda: self.__send_button(self.entry_chat_msg.get()))
        button_send_msg.pack(side=LEFT, expand=1)
        self.frame.pack()
        
        #self.notebook.insert(0, self.frame, text=self.name)

    def update_chat(self):
        self.text_field.config(state=NORMAL)
        line_num = float(1.0)

        for post in self.log:
            post_entry = post[0]+ ' - ' + post[1]+': '+ post[2] + '\n'
            self.text_field.insert(str(line_num),post_entry)
            line_num = line_num + 1


if __name__ == '__main__':

    update = [['comtek',[['25-08-22 14:20','Faur','Hvem ved hvad klokken er ??'],['25-08-22 14:23','Pure Genie','14:27 why ??'],['25-08-22 14:24','Wrongside','Mads?'],['25-08-22 14:26','SnooGiraffe','Bajer!!!!']]], ['Secret',['07-11-2022', 'Anonymous', 'Its a secret!! Dont tell..']]]
    update2 = [['comtek2022',[['25-08-22 14:20','Faur','Hvem ved hvad klokken er ??'],['25-08-22 14:23','Pure Genie','14:27 why ??'],['25-08-22 14:24','Wrongside','Mads?'],['25-08-22 14:26','SnooGiraffe','Bajer!!!!']]], ['Secret',['07-11-2022', 'Anonymous', 'Its a secret!! Dont tell..']]]

    root = GUI()
    root.mainloop()