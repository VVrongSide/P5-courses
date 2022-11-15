import tkinter as tk
from tkinter import ttk

def handleTabChange(event):
    if notebook.select() == notebook.tabs()[-1]:
        index = len(notebook.tabs())-1
        frame = tk.Frame(notebook)
        notebook.insert(index, frame, text="<untitled>")
        notebook.select(index)

root = tk.Tk()

notebook = ttk.Notebook(root)
notebook.bind("<<NotebookTabChanged>>", handleTabChange)

notebook.pack(fill="both", expand=True)

# add a tab that creates new tabs when selected
frame = tk.Frame()
notebook.add(frame, text="+")

root.mainloop()
