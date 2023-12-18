import tkinter as tk
import tkinter.ttk as ttk


class View(ttk.Frame):
    def __init__(self, parent, controller, size):
        super().__init__(parent)
        self._parent = parent
        self._controller = controller
        for row in range(size[0]):
            self.rowconfigure(row, weight=1)
        for col in range(size[1]):
            self.columnconfigure(col, weight=1)
    
    def _initWidgets(self, title):
        ttk.Label(self, text=title, font=("Helvetica", 32), anchor="center").grid(row=0, column=0, sticky=tk.NSEW)
  
        
class MainView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, (4, 1))
        self._initWidgets()
        
    def _initWidgets(self):
        super()._initWidgets("Fitness")
        ttk.Button(self, text="Start", command=lambda: self._controller.update("exer_list")).grid(row=1, sticky=tk.NSEW)
        ttk.Button(self, text="Settings", command=lambda: self._controller.update("settings")).grid(row=2, sticky=tk.NSEW)
        ttk.Button(self, text="Exit", command=lambda: self._controller.update("quit")).grid(row=3, sticky=tk.NSEW)
        
        self.rowconfigure(0, weight=2)


class SettingsView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, (1, 1))
        self._initWidgets()
        
    def _initWidgets(self):
        super()._initWidgets("Settings")


class ExerciseListView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, (6, 1))
        self._initWidgets()
        
    def _initWidgets(self):
        super()._initWidgets("Fitness")
        ttk.Button(self, text="Lorem", command=lambda: self._controller.update("Lorem")).grid(row=1, column=0, sticky=tk.NSEW)
        ttk.Button(self, text="Lorem", command=lambda: self._controller.update("Lorem")).grid(row=2, column=0, sticky=tk.NSEW)
        ttk.Button(self, text="Lorem", command=lambda: self._controller.update("Lorem")).grid(row=3, column=0, sticky=tk.NSEW)
        ttk.Button(self, text="Lorem", command=lambda: self._controller.update("Lorem")).grid(row=4, column=0, sticky=tk.NSEW)
        ttk.Button(self, text="←", command=lambda: 
            self._controller.update("back")).grid(row=5, column=0, sticky=tk.E, padx=(0, self._parent.winfo_width()*1/100))
        
        
class PreviewView(View):
    pass
        
        
class RecorderView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, (1, 1))
        self.background = "black"
        self._initWidgets()
        
    def _initWidgets(self):
        self.display = ttk.Label(self, background="black")
        self.display.pack(expand=1, fill="both")
