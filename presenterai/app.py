import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

from .views import *

class App(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Setup window
        super().__init__()
        self.attributes("-fullscreen", True)
        self.overrideredirect(True)
        self.resizable(False, False)
        
        # Setup views
        TextResults(self)
        
        self.mainloop()

"""import openai

messages = [ {"role": "system", "content": "You are a intelligent assistant"} ]
"""