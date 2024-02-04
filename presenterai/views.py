import customtkinter as ctk

from util.view import View


class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, border_color="red", border_width=10)
        self.text = ctk.StringVar(value="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        self.label = ctk.CTkLabel(self, 
            textvariable=self.text, 
            justify="left", 
            wraplength=self.winfo_screenwidth()*0.9,
            font=("Calibri", 34))
        self.label.pack(expand=True, fill="both")
        
class TextResults(View):
    def __init__(self, parent):
        super().__init__("Editing", parent)
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight= self.winfo_screenheight()
        self.text_frame = ScrollFrame(self)
        self.text_frame.pack(expand=True, fill="x", padx=10)
        scroll_buttons = self.get_scroll_buttons()
        scroll_buttons.pack(expand=True, fill="x", padx=self.screenwidth*0.1, pady=10)
        
    def get_scroll_buttons(self):
        frame = ctk.CTkFrame(self)
        
        # Create buttons
        up_button = ctk.CTkButton(frame, 
            text="^", 
            text_color="white", 
            command=self.text_frame._parent_canvas.yview_scroll(10, "units"))
        down_button = ctk.CTkButton(frame, 
            text="^", 
            text_color="white", 
            command=self.text_frame._parent_canvas.yview_scroll(10, "units"))
        
        # Place buttons
        up_button.pack(side="left", expand=True, fill="y", padx=self.screenwidth*0.05, ipadx=self.screenwidth*0.15)
        down_button.pack(side="left", expand=True, fill="y")
        
        return frame