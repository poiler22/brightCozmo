from tkinter import *
#from PIL import ImageTk, Image
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
import time
import os

root = Tk()
root.geometry("1050x800+300+150")
root.resizable(width=True, height=True)


def openfn():
    startchat = filedialog.askopenfilename(title='open')
    return startchat


def open_voice():
    import CozmoMainCode

    CozmoMainCode.mainLoop()


btn0 = Button(root, text='Start Chat', command=open_voice).pack()
btn1 = Button(root, text='Edit', command=open_voice).pack()

path = 'Doraemon.jpeg'
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")

root.mainloop()
