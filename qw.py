import tkinter as tk
from PIL import ImageTk

root = tk.Tk()
def make_button():
    b = tk.Button(root)
    image = ImageTk.PhotoImage(file="Doraemon.jpeg")
    b.config(image=image)
    b.image = image
    b.pack()
make_button()
root.mainloop()