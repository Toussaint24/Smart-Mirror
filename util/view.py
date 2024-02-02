import tkinter as tk
#import tkinter.ttk as ttk
import customtkinter as ctk


class View(ctk.CTkFrame):
    view_list = {}
    def __init__(self, name: str, parent: ctk.CTk, controller):
        super().__init__(parent)
        self._parent = parent
        self._controller = controller
        self.view_list[name] = self
        self.grid(row=0, column=0, sticky=tk.NSEW)
    
    