import tkinter as tk
# import tkinter.ttk as ttk
import customtkinter as ctk
from util.view import View
        
class MainView(View):
    def __init__(self, parent: tk.Tk, controller):
        super().__init__("main", parent, controller)
        self._initWidgets()
        ctk.set_appearance_mode("dark")

    def _initWidgets(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        for row in range(4):
            self.rowconfigure(row, weight=1)
        for col in range(1):
            self.columnconfigure(col, weight=1)
        self.rowconfigure(0, weight=2)
        
        ctk.CTkLabel(self, text= 'FITNESS', font=("Helvetica", 145), anchor="center").grid(row=0, column=0, sticky=tk.NSEW)
        ctk.CTkButton(self, text="Start", command=lambda: self._controller.set_view("exer_list"),
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 150,
                      width= 220
                      ).grid(row=1)
        ctk.CTkButton(self, text="Setting",command=lambda: self._controller.set_view("settings"),
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 150,
                      width= 220).grid(row=2)
        ctk.CTkButton(self, text="Exit", command=self._controller.quit,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 150,
                      width= 220).grid(row=3)


class SettingsView(View):
    def __init__(self, parent, controller):
        super().__init__("settings", parent, controller)
        self._initWidgets()
        ctk.set_appearance_mode("dark")

    def _initWidgets(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        for row in range(6):
            self.rowconfigure(row, weight=1)
        for col in range(1):
            self.columnconfigure(col, weight=1)

        ctk.CTkLabel(self, text= 'SETTING', font=("Helvetica", 115), anchor="center").grid(row=0, column=0, sticky=tk.NSEW)
        ctk.CTkButton(self, text="Lorem", command=self._controller.record,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 150,
                      width= 220
                      ).grid(row=1)
        ctk.CTkButton(self, text="Lorem", command=self._controller.record,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=2)
        ctk.CTkButton(self, text="Lorem",command=self._controller.record,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=3)
        ctk.CTkButton(self, text="Lorem", command=self._controller.record,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=4)

        ctk.CTkButton(self, text="←", command=lambda: self._controller.set_view("main"),
            fg_color= '#000',
            text_color='#ffffff',
            hover_color= '#bcf5e4',
            corner_radius = 27,
            border_color='#ffffff',
            border_width= 2).grid(row=5, column=0, sticky=tk.E, padx=(0, self._parent.winfo_width()*1/100))
        
       
        
class ExerciseListView(View):
    def __init__(self, parent, controller):
        super().__init__("exer_list", parent, controller)
        self._initWidgets()
        ctk.set_appearance_mode("dark")
    def _initWidgets(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        for row in range(6):
            self.rowconfigure(row, weight=1)
        for col in range(1):
            self.columnconfigure(col, weight=1)

        ctk.CTkLabel(self, text= 'EXERCISE', font=("Helvetica", 115), anchor="center").grid(row=0, column=0, sticky=tk.NSEW)
        ctk.CTkButton(self, text="Lorem", command=self._controller.record,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200
                      ).grid(row=1)
        ctk.CTkButton(self, text="Lorem", command=self._controller.record,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=2)
        ctk.CTkButton(self, text="Lorem",command=self._controller.record,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=3)
        ctk.CTkButton(self, text="Lorem", command=self._controller.record,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=4)

        ctk.CTkButton(self, text="←", command=lambda: self._controller.set_view("main"),
            fg_color= '#000',
            text_color='#ffffff',
            hover_color= '#bcf5e4',
            corner_radius = 27,
            border_color='#ffffff',
            border_width= 2).grid(row=5, column=0, sticky=tk.E, padx=(0, self._parent.winfo_width()*1/100))
        
       
class PreviewView(View):
    pass
        
        
class RecorderView(View):
    def __init__(self, parent, controller):
        super().__init__("recorder", parent, controller)
        self.background = "black"
        self._initWidgets()
    def _initWidgets(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.display = tk.Canvas(self, background='#000')
        self.display.grid(row=0, column=0, sticky="nsew")
    
        ctk.CTkButton(self, text="Begin",
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 120,
                      width= 100).grid(row=0)
        
        ctk.CTkButton(self, text="←", command=lambda: self._controller.set_view("main"),
            fg_color= '#000',
            text_color='#ffffff',
            hover_color= '#bcf5e4',
            corner_radius = 27,
            border_color='#ffffff',
            border_width= 2).grid(sticky=tk.E, padx=(0, self._parent.winfo_width()*1/100))
        