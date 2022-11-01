from main_page import DefaultGUI
import tkinter as tk
from tkinter import ttk


class NoChatGUI(DefaultGUI):
    def __init__(self):
        super().__init__()
        self.resizable(0,0)

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
        else:
            self.label_error.config(text="Invalied invitation code", fg="red")

    def __create_chat(self):
        entered_invite_code = self.entry_invite_code.get()
        print(entered_invite_code)
        if entered_invite_code == 'Connie':
            self.label_error.config(text="New chat of Connie! is ready", fg="#211A52")
        else:
            self.label_error.config(text="Invalied invitation code", fg="red")

if __name__=="__main__":
    root = NoChatGUI()
    root.mainloop()