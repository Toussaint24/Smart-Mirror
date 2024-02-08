import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk


class View(ctk.CTkFrame):
    def __init__(self, name: str, parent: tk.Tk):
        super().__init__(parent, bg_color="black",fg_color="black")
        self._parent = parent
        self._parent.view_list[name] = self
        # self.canvas = ctk.CTkCanvas(self,background = "black")
        # self.canvas.pack(expand=True, fill='both')
        #self.frame = ctk.CTkFrame(self,fg_color="black")
        self.place(relwidth=1.0, relheight=1.0)
        self.pack_propagate(False)

        
    def _init_widgets(self):
        self.button = ctk.CTkButton(self, 
            text="X", 
            font=("Helvetica",20),
            corner_radius=10,
            fg_color="#f51402", 
            hover_color="#fc796f", 
            text_color="white", 
            command=self._parent.quit)
        self.button.place(relx=1.0, rely=0.0, anchor="ne", relwidth=0.060, relheight=0.05)