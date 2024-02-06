import customtkinter as ctk

from util.view import View


class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = ctk.StringVar(value="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        self.label = ctk.CTkLabel(self, 
            textvariable=self.text, 
            justify="left", 
            wraplength=self.winfo_screenwidth()*0.6,
            font=("Calibri", 34))
        self.label.pack(expand=True, fill="both")
        
class Results(View):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        tabs = self.get_tabs()
        tabs.pack(side="bottom", fill="x", ipady=self.screenheight*0.04)
        
    def get_tabs(self):
        frame = ctk.CTkFrame(self)
        
        stats_button = ctk.CTkButton(frame, 
            text="Results",
            corner_radius=1,
            command=lambda: self._parent.set_view("stats"))
        editing_button = ctk.CTkButton(frame, 
            text="Editing",
            corner_radius=1,
            command=lambda: self._parent.set_view("editing"))
        
        stats_button.pack(side="left", expand=True, fill="both", padx=0.01)
        editing_button.pack(side="left", expand=True, fill="both", padx=0.01)
        
        return frame

        
class Editing(Results):
    def __init__(self, parent):
        super().__init__("editing", parent)
        
        # Create widgets
        self.text_frame = ScrollFrame(self)
        scroll_buttons = self.get_scroll_buttons()
        editing_options = self.get_editing_options()
        
        # Place widgets
        self.text_frame.pack(
            padx=self.screenwidth*0.05, 
            pady=self.screenheight*0.03,
            ipadx=self.screenwidth*0.25, 
            ipady=self.screenheight*0.13)
        scroll_buttons.pack(fill="x", padx=self.screenwidth*0.25, ipady=self.screenheight*0.02)
        editing_options.pack(fill="both", expand=True, padx=self.screenwidth*0.25, pady=self.screenheight*0.03)
        
    def get_scroll_buttons(self):
        frame = ctk.CTkFrame(self, fg_color="#2A2B2B")
        
        # Create buttons
        up_button = ctk.CTkButton(frame, 
            text="^", 
            text_color="white", 
            command=lambda: self.text_frame._parent_canvas.yview_scroll(10, "units"))
        down_button = ctk.CTkButton(frame, 
            text="v", 
            text_color="white", 
            command=lambda: self.text_frame._parent_canvas.yview_scroll(-10, "units"))
        
        # Place buttons
        padx = self.screenwidth*0.005
        up_button.pack(side="left", expand=True, fill="both", padx=padx)
        down_button.pack(side="left", expand=True, fill="both", padx=padx)
        
        return frame
    
    def get_editing_options(self):
        frame = ctk.CTkFrame(self, fg_color="#2A2B2B")
        
        # Create grid
        frame.rowconfigure((0, 1), weight=1)
        frame.columnconfigure((0, 1), weight=1)
        
        # Create options
        enhance_option = ctk.StringVar(value="")
        enhancement_options = ctk.CTkComboBox(frame, 
            values=["grammar", "phrasing"],
            font=("Calibri", 40),
            dropdown_font=("Calibri", 40),
            height=self.screenheight*0.1,
            variable=enhance_option)
        suggest_option = ctk.StringVar(value="")
        suggestion_options = ctk.CTkComboBox(frame,
            values=["suggestions", "feedback", "counters"],
            font=("Calibri", 40),
            dropdown_font=("Calibri", 40),
            height=self.screenheight*0.1,
            variable=suggest_option)
        
        # Create buttons
        enhance_button = ctk.CTkButton(frame, text="Enhance", command=lambda: self._parent.enhance(enhance_option.get()))
        suggest_button = ctk.CTkButton(frame, text="Suggest", command=lambda: self._parent.suggest(suggest_option.get()))
        
        # Place widgets
        enhancement_options.grid(row=0, column=0, sticky="ew", padx=self.screenwidth*0.005)
        suggestion_options.grid(row=1, column=0, sticky="ew", padx=self.screenwidth*0.005)
        
        enhance_button.grid(row=0, column=1, sticky="ew", padx=self.screenwidth*0.005, ipady=self.screenheight*0.05)
        suggest_button.grid(row=1, column=1, sticky="ew", padx=self.screenwidth*0.005, ipady=self.screenheight*0.05)
        
        return frame
        
    
class Stats(Results):
    def __init__(self, parent):
        super().__init__("stats", parent)
        self.add_stat("Number of filler words:", "X")
        self.add_stat("Filler word frequency:", "X")
        
        retry = ctk.CTkButton(self, text="Retry", command=lambda: print("Retrying"))
        retry.pack(side="bottom", pady=self.screenheight*0.02, ipadx=self.screenwidth*0.07, ipady=self.screenheight*0.02)
        
    def add_stat(self, desc: str, result: str):
        self.get_stat(desc, result).pack(fill="x", pady=self.screenheight*0.005)
        
    def get_stat(self, desc: str, result: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self, fg_color="transparent", border_color="red")
        
        desc_label = ctk.CTkLabel(frame, text=desc, fg_color="transparent", font=("Calibri", 60), anchor="w",)
        result_label = ctk.CTkLabel(frame, text=result, fg_color="transparent", text_color="red", font=("Calibri", 60))
        
        desc_label.pack(side="left", padx=self.screenwidth*0.05)
        result_label.pack(side="right", padx=self.screenwidth*0.2)
        
        return frame