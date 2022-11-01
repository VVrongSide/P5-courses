from main_gui import DefaultGUI
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import time
import threading

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
        Encode message and send over socket to the server.
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
        Create thread to receive messages from server and insert them to history chat.
        """

if __name__=="__main__":


    test4 = ChatGUI('Connie')
    test4.mainloop()
    