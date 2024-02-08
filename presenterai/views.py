import customtkinter as ctk

from util.view import View

#GUI for the recording
class HomeScreen(View):
    def __init__(self, parent):
        super().__init__("home", parent)
        self._initWidgets()

    def _initWidgets(self):
        # Create grid
        self.rowconfigure((0,1,2,3), weight=1)
        self.columnconfigure(0,weight=1)
        # Create widgets
        app_title = ctk.CTkLabel(self, 
            text="P R E S E N T E R  A I",  
            font=("Helvetica",82),
            text_color="white",
            fg_color="black")
        
        desc_action = ctk.CTkLabel(self, 
            text="P r e s s  t o  b e g i n",  
            font=("Helvetica",50),
            text_color="white",
            fg_color="black")

        start_button = ctk.CTkButton (self, text= "⦿",
                                        font=("Helvetica",90),
                                        anchor = "center",
                                        height= 49, width=45,
                                        corner_radius= 50,
                                        text_color="#e8e4e3",
                                        fg_color="#eb6565",
                                        hover_color= '#fc796f') 
        # Place widgets
        app_title.grid(row = 0, column = 0, rowspan = 2)
        desc_action.grid(row = 2, column = 0)
        start_button.grid(row = 3,column = 0)
        super()._init_widgets()

class RecordingScreen(View):
    def __init__(self, parent):
        super().__init__("recording_screen", parent)
        self._initWidgets()

    def _initWidgets(self):
        # Create grid
        self.columnconfigure(0,weight=1)
        self.rowconfigure((0,1,2,3), weight=1, uniform='b')
        # Create widgets

        desc_action = ctk.CTkLabel(self,
                                   text="R e c o r d i n g  . . .",
                                   font=("Helvetica",85),
                                   text_color="white",
                                   fg_color="black")
        desc_stop_action = ctk.CTkLabel(self,
                                   text="P r e s s  t o  f i n i s h",
                                   font=("Helvetica",50),
                                   text_color="white",
                                   fg_color="black")

        stop_button = ctk.CTkButton (self, text= "⏸",
                                     font=("Helvetica",90),
                                     anchor = "center",
                                     height= 45, width=20,
                                     corner_radius= 100,
                                     text_color="#e8e4e3",
                                     fg_color="#eb6565",
                                     hover_color= '#fc796f') 
        # Place widgets
        desc_action.grid(row = 1, column = 0)
        desc_stop_action.grid(row = 2,column = 0 )
        stop_button.grid(row = 3,column = 0)
        super()._init_widgets()

class StopScreen(View):
    def __init__(self, parent):
        super().__init__("stop_screen", parent)
        self._initWidgets()

    def _initWidgets(self):
        # Create grid
        self.columnconfigure((0,1),weight=1)
        self.rowconfigure((0,1,2,3), weight=1, uniform='c')
        # Create widgets

        desc_action = ctk.CTkLabel(self,
                                   text="L e t ' s  c o n t i n u e d  . . .",
                                   font=("Helvetica",85),
                                   text_color="white",
                                   fg_color="black")

        resume_button = ctk.CTkButton (self, text= "Resume",
                                     font=("Helvetica",50),
                                     anchor = "center",
                                     height= 120, width=230,
                                     corner_radius= 50,
                                     text_color="#e8e4e3",
                                     fg_color="#eb6565",
                                     hover_color= '#fc796f',
                                    ) 
        done_button = ctk.CTkButton (self, text= "Done",
                                     font=("Helvetica",50),
                                     anchor = "center",
                                     height= 120, width=290,
                                     corner_radius= 50,
                                     text_color="#e8e4e3",
                                     fg_color="#eb6565",
                                     hover_color= '#fc796f') 
        # Place widgets
        desc_action.grid(row = 1, column = 0,columnspan = 2)
        resume_button.grid(row = 3,column = 0)
        done_button.grid(row = 3, column = 1)
        super()._init_widgets()

#GUI for the speech
class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = ctk.StringVar(value=
            """Winston Churchill is widely regarded as one of the most effective leaders of the 20th century, particularly for his leadership during World War Il. However, what made Churchill's leadership style so successful? One way to answer this question is by
            examining his leadership style through Blake and Mouton's Managerial Leadership Grid. The Managerial Leadership Grid is a tool that assesses a leader's concern for task completion and concern for people, resulting in five leadership styles: impoverished, country club, middle-of-the-road, team, and authority-compliance. Based on his actions and behaviors during World War Il, it is likely that Churchill's leadership style falls under the authority-compliance category of the Grid. This style is characterized by a high
            concern for task completion and a low concern for people. Despite its limitations, Churchill's authority-compliance leadership style proved highly effective during the war. He was able to rally the British people and coordinate the country's war efforts, ultimately leading to victory over Nazi Germany. However, this style also had its drawbacks, such as the strain it put on Churchill's relationships with his
            subordinates and the potential for burnout. While Churchill's leadership style may not be suitable for all contexts, it provides valuable insights into the complex interplay between task completion and concern for people in leadership. By using the Managerial Leadership Grid to analyze Churchill's leadership style, we can learn from his successes and limitations and apply these lessons to
            contemporary leadership development. In conclusion, Winston Churchill's leadership during World War II exemplifies the authority-compliance leadership style as identified by Blake and Mouton's Managerial Leadership Grid. While this style may not be appropriate for all situations, it proved highly effective in rallying a country and leading it to victory. By examining Churchill's leadership style through the Grid, we can gain valuable insights into the role of task completion and concern for people in effective leadership, and apply these lessons to contemporary
            organizational contexts.""")
        self.label = ctk.CTkLabel(self, 
            textvariable=self.text, 
            justify="left", 
            font=("Calibri", 34))
        self.label.pack(expand=True, fill="both")
        
    def _update_dimensions(self):
        self.update_idletasks()
        self.height = self.winfo_height()
        self.width = self.winfo_width()
        self.label.configure(wraplength=self.width)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self._update_dimensions()
        print(self.width, self.height)
        
    def place(self, **kwargs):
        super().place(**kwargs)
        self._update_dimensions()
        print(self.width, self.height)
        
class ScrollButtons(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,fg_color="black")
        self.parent = parent
        
        # Create buttons
        up_button = ctk.CTkButton(self, 
            text="^",
            font=("Courier New", 45),
            fg_color= "black",
            text_color= "#eb6565",
            hover_color="#858282",
            height= 80, 
            width= 5,
            corner_radius= 100,
            border_color="white",
            border_width=1,
            command=lambda: self.parent.text_frame._parent_canvas.yview_scroll(-10, "units"))
        down_button = ctk.CTkButton(self, 
            text="V",
            font=("Courier New", 23), 
            fg_color= "black",
            text_color= "#eb6565",
            hover_color="#858282",
            border_color="white",
            border_width=1,
            height= 80, 
            width= 70,
            corner_radius= 200, 
            command=lambda: self.parent.text_frame._parent_canvas.yview_scroll(10, "units"))
        
        # Place buttons
        padx = self.winfo_screenwidth()*0.005
        up_button.pack(side="left", expand=True, padx=padx)
        down_button.pack(side="left", expand=True, padx=padx)
    
        
class Prompt(ctk.CTkFrame):
    def __init__(self, parent, message: str = ""):
        super().__init__(parent, corner_radius=27,bg_color="#535454",fg_color="#535454")
        self._parent = parent
        self.pack_propagate(False)
        self.place(relx=0.3, rely=0.4, relwidth=0.6, relheight=0.5, anchor="center")
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.text_frame = ScrollFrame(self)
        self.text_frame.text.set(message)
        self.text_frame.label.configure(text_color="white")
        self.text_frame.pack(
            expand=True, 
            fill="both",
            padx=self.width*0.05, 
            pady=self.height*0.03, 
        )
        self.scroll_buttons = ScrollButtons(self)
        self.scroll_buttons.pack(pady = 4,fill="x")
        self.confirm = ctk.CTkButton(self, 
            text="Confirm",
            font=("Courier New", 29), 
            fg_color="#eb6565", 
            border_color="white", 
            border_width=2, 
            text_color="white",
            height= 30,
            width= 50,
            hover_color="#d49292",
            command=self.hide)
        self.confirm.pack(pady= 10)
    
    def show(self):
        self.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.767, anchor="center")
        self.tkraise()
    
    def hide(self):
        self.place_forget()
        
class Results(View):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        tabs = self.get_tabs()
        tabs.pack(side="bottom", fill="x",ipady=self.screenheight*0.02)
        super()._init_widgets()
        
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
        scroll_buttons = ScrollButtons(self)
        editing_options = self.get_editing_options()
        
        # Place widgets
        self.text_frame.pack(
            padx=self.screenwidth*0.05, 
            pady=self.screenheight*0.03,
            ipadx=self.screenwidth*0.25, 
            ipady=self.screenheight*0.13)
        scroll_buttons.pack(fill="x", padx=self.screenwidth*0.25, ipady=self.screenheight*0.02)
        editing_options.pack(fill="both", expand=True, padx=self.screenwidth*0.25, pady=self.screenheight*0.03)
        super()._init_widgets()
    
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
                                       border_color="#9e9a99",
                                       border_width= 1,
                                       width=200,
            
                                       command=lambda: self._parent.edit(enhance_option.get(), self.text_frame.text))
        suggest_button = ctk.CTkButton(frame, text="Suggest",
                                       font=("Courier New", 35),
                                       fg_color= "black",
                                       text_color= "white",
                                       hover_color="#858282",
                                       border_color="#9e9a99",
                                       border_width= 1,
                                       width=200,
                                       command=lambda: self._parent.edit(suggest_option.get(), self.text_frame.text))
        
        # Place widgets
        enhancement_options.grid(row=0, column=0, sticky="ew", padx=self.screenwidth*0.005)
        suggestion_options.grid(row=1, column=0, sticky="ew", padx=self.screenwidth*0.005)
        
        enhance_button.grid(row=0, column=1, padx=self.screenwidth*0.005,ipady=self.screenheight*0.005)
        suggest_button.grid(row=1, column=1, padx=self.screenwidth*0.005, ipady=self.screenheight*0.005)
        
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