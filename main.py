import tkinter as tk
import customtkinter as ctk
from fitnessmonitor.app import App

root = ctk.CTk()
root.attributes("-fullscreen", True)
app = App(root)
root.mainloop()