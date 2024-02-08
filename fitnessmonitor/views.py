import tkinter as tk
# import tkinter.ttk as ttk
import customtkinter as ctk
from util.view import View
        
class Main(View):
    def __init__(self, parent: tk.Tk):
        super().__init__("main", parent)
        self._initWidgets()

    def _initWidgets(self):
        # Create grid
        self.rowconfigure(0, weight=2)
        self.rowconfigure((1, 2, 3), weight=1)
        self.columnconfigure(0, weight=1)
        
        # Create widgets
        ctk.CTkLabel(self, text= 'F I T N E S S', font=("Helvetica", 145), anchor="center",bg_color="black").grid(row=0, column=0, sticky=tk.NSEW)
        ctk.CTkButton(self, text="Start", command=lambda: self._parent.set_view("exer_list"),
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
        ctk.CTkButton(self, text="Setting",command=lambda: self._parent.set_view("settings"),
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 150,
                      width= 220).grid(row=2)
        ctk.CTkButton(self, text="Exit", command=self._parent.quit,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 150,
                      width= 220).grid(row=3)
        
        super()._init_widgets()


class Settings(View):
    def __init__(self, parent):
        super().__init__("settings", parent)
        self._initWidgets()

    def _initWidgets(self):
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text= 'S E T T I N G', font=("Helvetica", 115),bg_color="black", anchor="center").grid(row=0, column=0, sticky=tk.NSEW)
        ctk.CTkButton(self, text="Coming soon...", command=None,
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
        ctk.CTkButton(self, text="Coming soon...", command=None,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=2)
        ctk.CTkButton(self, text="Coming soon...",command=None,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=3)
        ctk.CTkButton(self, text="Coming soon...", command=None,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=4)

        ctk.CTkButton(self, text="←", command=lambda: self._parent.set_view("main"),
            fg_color= '#000',
            text_color='#ffffff',
            hover_color= '#bcf5e4',
            corner_radius = 27,
            border_color='#ffffff',
            border_width= 2).grid(row=5, column=0, sticky=tk.E, padx=(0, self._parent.winfo_width()*1/100))
        
        super()._init_widgets()
       
        
class ExerciseList(View):
    def __init__(self, parent):
        super().__init__("exer_list", parent)
        self._initWidgets()
        
    def _initWidgets(self):
        # Create grid
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.columnconfigure(0, weight=1)

        # Create widgets
        ctk.CTkLabel(self, text= 'E X E R C I S E', font=("Helvetica", 115),bg_color="black", anchor="center").grid(row=0, column=0, sticky=tk.NSEW)
        ctk.CTkButton(self, text="Bicep Curl", command=self._parent.record,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 330
                      ).grid(row=1)
        ctk.CTkButton(self, text="Coming soon...", command=None,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=2)
        ctk.CTkButton(self, text="Coming soon...",command=None,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=3)
        ctk.CTkButton(self, text="Coming soon...", command=None,
                      fg_color= '#000',
                      text_color='#ffffff',
                      hover_color= '#bcf5e4',
                      corner_radius = 27,
                      border_color='#ffffff',
                      border_width= 2,
                      font=("Helvetica", 42),
                      height= 130,
                      width= 200).grid(row=4)

        ctk.CTkButton(self, text="←", command=lambda: self._parent.set_view("main"),
            fg_color= '#000',
            text_color='#ffffff',
            hover_color= '#bcf5e4',
            corner_radius = 27,
            border_color='#ffffff',
            border_width= 2).grid(row=5, column=0, sticky=tk.E, padx=(0, self._parent.winfo_width()*1/100))
        
        super()._init_widgets()
        
        
class Recorder(View):
    def __init__(self, parent):
        super().__init__("recorder", parent)
        self.configure(fg_color="black")
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        self._initWidgets()
        
    def _initWidgets(self):
        self.reps_counter = ctk.CTkLabel(self, corner_radius=27,font=("Helvetica", 40),fg_color="#133638", text_color= "white",textvariable=self._parent.counter)
        self.pos_indicator = ctk.CTkLabel(self, corner_radius=27,font=("Helvetica", 40), fg_color="#a1321a",text_color= "white",textvariable=self._parent.position_str)
        self.msg_board = ctk.CTkLabel(self, corner_radius=27,font=("Helvetica", 25), fg_color="#133638",text_color= "white", textvariable=self._parent.message)
        
        self.reps_counter.pack(
            anchor=tk.W, 
            padx=self.screenwidth*0.05, 
            pady=self.screenwidth*0.05,
            ipadx=self.screenwidth*0.01,
            ipady=self.screenheight*0.01)
        self.pos_indicator.pack(
            anchor=tk.W, 
            padx=self.screenwidth*0.05,
            ipadx=self.screenwidth*0.005,
            ipady=self.screenheight*0.005)
        self.msg_board.place(anchor="ne", relx=0.95, rely=0.1, relwidth=0.3, relheight=0.15)