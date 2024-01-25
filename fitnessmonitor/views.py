import tkinter as tk
import tkinter.ttk as ttk

from util.view import View
        
class MainView(View):
    def __init__(self, parent: tk.Tk, controller):
        super().__init__("main", parent, controller)
            
        self._initWidgets()
        
    def _initWidgets(self):
        for row in range(4):
            self.rowconfigure(row, weight=1)
        for col in range(1):
            self.columnconfigure(col, weight=1)
        self.rowconfigure(0, weight=2)
        
        super()._initWidgets("Fitness")
        ttk.Button(self, text="Start", command=lambda: self._controller.set_view("exer_list")).grid(row=1, sticky=tk.NSEW)
        ttk.Button(self, text="Settings", command=lambda: self._controller.set_view("settings")).grid(row=2, sticky=tk.NSEW)
        ttk.Button(self, text="Exit", command=self._controller.quit).grid(row=3, sticky=tk.NSEW)


class SettingsView(View):
    def __init__(self, parent, controller):
        super().__init__("settings", parent, controller)
        self._initWidgets()
        
    def _initWidgets(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        super()._initWidgets("Settings")


class ExerciseListView(View):
    def __init__(self, parent, controller):
        super().__init__("exer_list", parent, controller)
        self._initWidgets()
        
    def _initWidgets(self):
        for row in range(6):
            self.rowconfigure(row, weight=1)
        for col in range(1):
            self.columnconfigure(col, weight=1)
        super()._initWidgets("Fitness")
        ttk.Button(self, text="Lorem", command=self._controller.record).grid(row=1, column=0, sticky=tk.NSEW)
        ttk.Button(self, text="Lorem", command=self._controller.record).grid(row=2, column=0, sticky=tk.NSEW)
        ttk.Button(self, text="Lorem", command=self._controller.record).grid(row=3, column=0, sticky=tk.NSEW)
        ttk.Button(self, text="Lorem", command=self._controller.record).grid(row=4, column=0, sticky=tk.NSEW)
        ttk.Button(self, text="←", command=lambda: 
            self._controller.set_view("main")).grid(row=5, column=0, sticky=tk.E, padx=(0, self._parent.winfo_width()*1/100))
        
        
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
        self.display = tk.Canvas(self)
        self.display.grid(row=0, column=0, sticky="nsew")