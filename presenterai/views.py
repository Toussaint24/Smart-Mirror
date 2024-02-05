import customtkinter as ctk

from util.view import View


class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = ctk.StringVar(value="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        self.label = ctk.CTkLabel(self, 
            textvariable=self.text, 
            justify="left", 
            wraplength=self.winfo_screenwidth()*0.88,
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
            corner_radius=10,
            command=lambda: self.parent.set_view("stats"))
        editing_button = ctk.CTkButton(frame, 
            text="Editing",
            corner_radius=10,
            command=lambda: self.parent.set_view("edit"))
        
        stats_button.pack(side="left", expand=True, fill="both")
        editing_button.pack(side="left", expand=True, fill="both")
        
        return frame

        
class Editing(Results):
    def __init__(self, parent):
        super().__init__("Editing", parent)
        self.text_frame = ScrollFrame(self)
        self.text_frame.pack(fill="x", padx=self.screenwidth*0.05, pady=self.screenheight*0.03, ipady=self.screenheight*0.13)
        scroll_buttons = self.get_scroll_buttons()
        scroll_buttons.pack(fill="x", padx=self.screenwidth*0.25, ipady=self.screenheight*0.02)
        editing_options = self.get_editing_options()
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
        frame = ctk.CTkFrame(self, fg_color="#2A2B2B", border_color="red", border_width=10)
        
        # Create grid
        frame.rowconfigure((0, 1), weight=1)
        frame.columnconfigure((0, 1), weight=1)
        
        # Create options
        enhance_option = ctk.StringVar(value="")
        enhancement_options = ctk.CTkComboBox(frame, 
            values=["grammar", "phrasing"],
            font=("Calibri", 20),
            dropdown_font=("Calibri", 20),
            variable=enhance_option)
        suggest_option = ctk.StringVar(value="")
        suggestion_options = ctk.CTkComboBox(frame,
            values=["suggestions", "feedback", "counterarguments"],
            font=("Calibri", 20),
            dropdown_font=("Calibri", 20),
            variable=suggest_option)
        
        # Create buttons
        enhance_button = ctk.CTkButton(frame, text="Enhance", command=lambda: self.parent.enhance(enhance_option.get()))
        suggest_button = ctk.CTkButton(frame, text="Suggest", command=lambda: self.parent.suggest(suggest_option.get()))
        
        # Place widgets
        enhancement_options.grid(row=0, column=0, sticky="se")
        suggestion_options.grid(row=1, column=0, sticky="ne")
        
        enhance_button.grid(row=0, column=1, sticky="sw")
        suggest_button.grid(row=1, column=1, sticky="nw")
        
        return frame
    
class Stats(Results):
    def __init__(self, parent):
        super().__init__("stats", parent)