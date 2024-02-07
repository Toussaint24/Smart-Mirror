import customtkinter as ctk

from util.view import View

#GUI for the recording
class HomeScreen(View):
    def __init__(self,name, parent):
        super().__init__(name, parent)
        self._initWidgets()
        self.exit_button()
        exit_button(self)
        ctk.set_appearance_mode("dark")

    def _initWidgets(self):
        # Create grid
        self.rowconfigure(0,1,2,3, weight=1)
        self.columnconfigure(0,weight=1)
        # Create widgets
        app_title = ctk.CTkLabel(self, 
            text="P R E S E N T E R  A I",  
            font=("Helvetica",30),
            text_color="white",
            fg_color="black")
        
        desc_action = ctk.CTkLabel(self, 
            text="press to begin",  
            font=("Helvetica",20),
            text_color="white",
            fg_color="black")

        start_button = ctk.CTkButton (self, text= ".",
                                        font=("Helvetica",70),
                                        anchor = "center",
                                        height= 20, width=20,
                                        corner_radius= 20,
                                        text_color="#e8e4e3",
                                        fg_color="#f51402",
                                        hover_color= '#fc796f') 
        # Place widgets
        app_title.grid(row = 0, column = 0, rowspan = 2, sticky = 'nsew')
        desc_action.grid(row = 3, column = 0, sticky = 'nsew')
        start_button.grid(row = 3,column = 0)
    pass

class  exit_button(ctk.CTkButton):
    def __init__(self,parent):
        super().__init__(parent,text="X",  
            font=("Helvetica",20),
            text_color="white",
            fg_color="black",
            corner_radius= 10,
            text_color="white",
            fg_color="#f51402",
            hover_color= '#fc796f'
            )
        self.grid(row = 0, column = 0, rowspan = 2, sticky = 'ne')
    pass

class RecordingScreen(HomeScreen):
    def __init__(self, parent):
        super().__init__("recording_sreen", parent)
        self._initWidgets()
        self.exit_button()
        exit_button(self)
        ctk.set_appearance_mode("dark")
        

    def _initWidgets(self):
        # Create grid
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,1,2,3, weight=1, uniform='b')
        # Create widgets

        desc_action = ctk.CTkLabel(self,
                                   text="Recording...",
                                   font=("Helvetica",40),
                                   text_color="white",
                                   fg_color="black")

        stop_button = ctk.CTkButton (self, text= "||",
                                     font=("Helvetica",20),
                                     anchor = "center",
                                     height= 20, width=20,
                                     corner_radius= 10,
                                     text_color="#e8e4e3",
                                     fg_color="#f51402",
                                     hover_color= '#fc796f') 
        # Place widgets
        desc_action.grid(row = 1, column = 0, sticky = 'nsew')
        stop_button.grid(row = 3,column = 0)
    pass

class StopSreeen(RecordingScreen):
    def __init__(self, parent):
        super().__init__("stop_sreen", parent)
        self._initWidgets()
        self.exit_button()
        ctk.set_appearance_mode("dark")

    def _initWidgets(self):
        # Create grid
        self.columnconfigure(0,1,weight=1)
        self.rowconfigure(0,1,2,3, weight=1, uniform='c')
        # Create widgets

        desc_action = ctk.CTkLabel(self,
                                   text="Let's continued...",
                                   font=("Helvetica",40),
                                   text_color="white",
                                   fg_color="black")

        resume_button = ctk.CTkButton (self, text= "resume",
                                     font=("Helvetica",20),
                                     anchor = "center",
                                     height= 20, width=20,
                                     corner_radius= 5,
                                     text_color="#e8e4e3",
                                     fg_color="#f51402",
                                     hover_color= '#fc796f') 
        done_button = ctk.CTkButton (self, text= "done",
                                     font=("Helvetica",20),
                                     anchor = "center",
                                     height= 20, width=20,
                                     corner_radius= 5,
                                     text_color="#e8e4e3",
                                     fg_color="#f51402",
                                     hover_color= '#fc796f') 
        # Place widgets
        desc_action.grid(row = 1, column = 0,columnspan = 2,sticky = 'nsew')
        resume_button.grid(row = 3,column = 0)
        done_button.grid(row = 3, comlumn = 1)
        pass

#GUI for the speech
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
        tabs.pack(side="bottom", fill="x",ipady=self.screenheight*0.02)
        
    def get_tabs(self):
        frame = ctk.CTkFrame(self,bg_color="black")
        
        stats_button = ctk.CTkButton(frame, 
            text="Results",
            corner_radius=30,
            command=lambda: self._parent.set_view("stats"),
            font=("Courier New", 34),
            fg_color= "black",
            text_color= "white",
            hover_color="#858282",
            border_color="#eb6565",
            border_width=1,
            height= 30
      
            )
        editing_button = ctk.CTkButton(frame, 
            text="Editing",
            corner_radius=30,
            command=lambda: self._parent.set_view("editing"),
            font=("Courier New", 34),
            fg_color= "black",
            text_color= "white",
            hover_color="#858282",
            border_color="#eb6565",
            border_width=1,
            height= 30

            )
        
        stats_button.pack(side="left", expand=True, fill="both", padx=100)
        editing_button.pack(side="left", expand=True, fill="both", padx=100)
        
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
            font=("Courier New", 45),
            fg_color= "black",
            text_color= "#eb6565",
            hover_color="#858282",
            height= 80, 
            width= 70,
            corner_radius= 200,
            command=lambda: self.text_frame._parent_canvas.yview_scroll(10, "units"))
        down_button = ctk.CTkButton(frame, 
            text="V",
            font=("Courier New", 23), 
            fg_color= "black",
            text_color= "#eb6565",
            hover_color="#858282",
            height= 80, 
            width= 70,
            corner_radius= 200, 
            command=lambda: self.text_frame._parent_canvas.yview_scroll(-10, "units"))
        
        # Place buttons
        padx = self.screenwidth*0.005
        up_button.pack(side="left", expand=True, padx=padx)
        down_button.pack(side="left", expand=True, padx=padx)
        
        return frame
    
    def get_editing_options(self):
        frame = ctk.CTkFrame(self, fg_color="#000000")
        
        # Create grid
        frame.rowconfigure((0, 1), weight=1)
        frame.columnconfigure((0, 1), weight=1)
        
        # Create options
        enhance_option = ctk.StringVar(value="")
        enhancement_options = ctk.CTkComboBox(frame, 
            values=["Grammar", "Phrasing"],
            font=("Courier New", 35),
            text_color="white",
            dropdown_font=("Courier New", 26),
            fg_color="black",
            button_color="#eb6565",
            height=self.screenheight*0.1,
            variable=enhance_option)
        suggest_option = ctk.StringVar(value="")
        suggestion_options = ctk.CTkComboBox(frame,
            values=["Suggestions", "Feedback", "Counters"],
            font=("Courier New", 35),
            text_color="white",
            dropdown_font=("Courier New", 26),
            fg_color="black",
            button_color="#eb6565",
            height=self.screenheight*0.1,
            variable=suggest_option)
        
        # Create buttons
        enhance_button = ctk.CTkButton(frame, text="Enhance",
                                       font=("Courier New", 35),
                                       fg_color= "black",
                                       text_color= "white",
                                       hover_color="#858282",
                                       command=lambda: self._parent.enhance(enhance_option.get()))
        suggest_button = ctk.CTkButton(frame, text="Suggest",
                                       font=("Courier New", 35),
                                       fg_color= "black",
                                       text_color= "white",
                                       hover_color="#858282",
                                       command=lambda: self._parent.suggest(suggest_option.get()))
        
        # Place widgets
        enhancement_options.grid(row=0, column=0, sticky="ew", padx=self.screenwidth*0.005)
        suggestion_options.grid(row=1, column=0, sticky="ew", padx=self.screenwidth*0.005)
        
        enhance_button.grid(row=0, column=1, padx=self.screenwidth*0.005,ipady=self.screenheight*0.05)
        suggest_button.grid(row=1, column=1, padx=self.screenwidth*0.005, ipady=self.screenheight*0.05)
        
        return frame
        
    
class Stats(Results):
    def __init__(self, parent):
        super().__init__("stats", parent)
        self.add_stat("Number of filler words:", "X")
        self.add_stat("Filler word frequency:", "X")
        
        retry = ctk.CTkButton(self, text="Retry",
                              font=("Courier New", 35),
                              fg_color= "black",
                              text_color= "white",
                              hover_color="#858282",
                              corner_radius=50,
                              command=lambda: print("Retrying"))
        retry.pack(side="bottom", pady=self.screenheight*0.04, ipadx=self.screenwidth*0.07, ipady=self.screenheight*0.02)
        
    def add_stat(self, desc: str, result: str):
        self.get_stat(desc, result).pack(fill="x", pady=self.screenheight*0.002)
        
    def get_stat(self, desc: str, result: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self, fg_color="transparent", border_color="red")
        
        desc_label = ctk.CTkLabel(frame, text=desc,
                                  fg_color="transparent",
                                  font=("Courier New", 45),
                                  anchor="w",)
        result_label = ctk.CTkLabel(frame, text=result,
                                    fg_color="transparent",
                                    text_color="red",
                                    font=("Courier New", 45))
        
        desc_label.pack(side="left", padx=self.screenwidth*0.05,pady=self.screenheight*0.05)
        result_label.pack(side="right", padx=self.screenwidth*0.2,pady=self.screenheight*0.05)
        
        return frame