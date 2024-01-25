import tkinter as tk
import tkinter.ttk as ttk


class View(ttk.Frame):
    view_list = {}
    def __init__(self, name: str, parent: tk.Tk, controller):
        super().__init__(parent)
        self._parent = parent
        self._controller = controller
        self.view_list[name] = self
        self.grid(row=0, column=0, sticky=tk.NSEW)
    
    def _initWidgets(self, title: str):
        ttk.Label(self, text=title, font=("Helvetica", 32), anchor="center").grid(row=0, column=0, sticky=tk.NSEW)