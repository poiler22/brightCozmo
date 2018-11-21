import sys
import os
from tkinter import Tk, Label, Button

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    root.destroy()
    os.execl(python, python, * sys.argv)
    sys.executable
    os.execl(sys.executable, sys.executable, *sys.argv)

root = Tk()

Label(root, text="Hello World!").pack()
Button(root, text="Restart", command=restart_program).pack()

root.mainloop()