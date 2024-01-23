import tkinter as tk

from fitnessmonitor.app import App

root = tk.Tk()
root.attributes("-fullscreen", True)
app = App(root)
root.mainloop()