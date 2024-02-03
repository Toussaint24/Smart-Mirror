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
    
    def _init_widgets(self):
        self.button = ctk.CTkButton(self, text="X", fg_color="red", text_color="white", command=self._controller.quit)
        self.button.place(relx=1.0, rely=0.0, anchor="ne", relwidth=0.075, relheight=0.05)