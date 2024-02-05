import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

from .views import *

class App(ctk.CTk):
    view_list = {}
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Setup window
        super().__init__()
        self.attributes("-fullscreen", True)
        self.overrideredirect(True)
        self.resizable(False, False)
        
        # Setup views
        Editing(self)
        
        self.mainloop()
        
    def set_view(self, pointer: str):
        try:
            self.views_list[pointer].tkraise()
        except KeyError:
            raise ValueError(f"Unknown view '{pointer}'")
        
    def enhance(self):
        print("Enhancing")
        
    def suggest(self):
        print("Suggesting")

"""import openai

messages = [ {"role": "system", "content": "You are a intelligent assistant"} ]
"""