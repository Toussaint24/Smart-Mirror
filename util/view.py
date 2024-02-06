import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk


class View(ctk.CTkFrame):
    def __init__(self, name: str, parent: tk.Tk):
        super().__init__(parent)
        self._parent = parent
        self._parent.view_list[name] = self
        self.place(relwidth=1.0, relheight=1.0)
        self.pack_propagate(False)