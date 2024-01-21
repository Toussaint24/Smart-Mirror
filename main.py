import tkinter as tk

from fitnessmonitor.controller import App

root = tk.Tk()
root.attributes("-fullscreen", True)
print(root.winfo_screenheight())
print(root.winfo_screenwidth())
print(root.winfo_height())
print(root.winfo_width())
app = App(root)
root.mainloop()