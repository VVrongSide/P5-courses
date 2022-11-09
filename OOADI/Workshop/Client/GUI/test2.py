from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk


class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.second_window()
        self.pm_tabs = []

    def init_window(self):# Builds the UI for the main window

        self.n = ttk.Notebook(root)

        self.get_tabs_button = Button(self.textboxframe,
                                      width=20,
                                      text='Get Tab Names',
                                      command=lambda:self.get_tab_names())
        self.get_tabs_button.grid(row = 0,
                                  column= 1,
                                  padx=(5,5),
                                  pady=(5,150),
                                  sticky=N+S+E+W)

        self.n.add(self.textboxframe, text='Chat')
        self.n.grid(row=0, column=0, sticky=N+S+E+W)

    def second_window(self):# UI for second window

        self.get_tabs_button = Button(self.textboxframe,
                                      width=20,
                                      text='Get Tab Names',
                                      command=lambda:self.get_tab_names())
        self.get_tabs_button.grid(row = 0,
                                  column= 1,
                                  padx=(5,5),
                                  pady=(5,150),
                                  sticky=N+S+E+W)
        self.n.add(self.textboxframe, text='Second')



if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    root.mainloop()