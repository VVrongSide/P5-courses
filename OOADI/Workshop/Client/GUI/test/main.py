import tkinter as tk
from tkinter import ttk


class DefaultGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Encrypted chat')            # Title of window
        self.geometry('800x600')                # Window size        
        self.resizable(0,0)                     # Window is not resizable and both x and y directions.
        self.color = '#aed6f1'                  # Color 
        self.configure(bg=self.color)           # Set background color
        self.headline_font = ("FreeSans", 16)
        self.error_font = ("FreeSans", 14)
        self.tabControl = ttk.Notebook()   

class MainGUI(DefaultGUI):
    def __init__(self):
        super().__init__()

        self.button_create = tk.Button(text='Create account',font=self.headline_font,width=13,command=lambda: self.__new_window())
        self.button_create.pack()


    def __new_window(self):
        self.destroy()
        test = TabGUI()
        

class TabGUI(DefaultGUI):
    def __init__(self):
        super().__init__()
        self.new_tab = tk.Frame(self.tabControl)
        
        self.tabControl.add(self.new_tab, text='+')
        self.tabControl.pack(expand=1, fill=tk.BOTH)

        self.frame = tk.Frame()
        self.button_tab = tk.Button(self.frame, text='Create tab',font=self.headline_font,width=13,command=lambda: self.__new_tab())
        self.button_tab.pack()
        self.tab_name = tk.Entry(self.frame)
        self.tab_name.pack()
        self.frame.pack(expand=True)

        def __new_tab(self, name):
            if notebook.select() == notebook.tabs()[-1]:
                index = len(notebook.tabs())-1
                frame = tk.Frame(notebook)
                notebook.insert(index, frame, text="<untitled>")
                notebook.select(index)



if __name__=="__main__":
    test = MainGUI()
    test.mainloop()