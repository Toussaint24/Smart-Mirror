import customtkinter as ctk
from openai import OpenAI

client = OpenAI()
import tkinter as tk
from tkinter import ttk

from recorder.audio import AudioRecorder
from .views import *

enhancements_prompts = {
    "Grammar": "Can you edit the grammar in my essay?",
    "Phrasing": "Can you edit the phrasing in my essay to sound more impressive?"
}
suggestion_prompts = {
    "Suggestions": "Can you give me suggestions to improve my essay?",
    "Feedback": "Can you give me feedback on my essay?",
    "Counters": "What are some counterarguments to the main points in my essay?",
}

class App(ctk.CTk):
    view_list = {}
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Init models
        self.messages = [ {"role": "system", "content": "You are a intelligent assistant"} ]
        
        # Setup window
        super().__init__(fg_color= "black")
        self.attributes("-fullscreen", True)
        self.attributes("-type", "splash")
        
        # Setup views
        HomeScreen(self)
        RecordingScreen(self)
        StopScreen(self)
        Editing(self)
        Stats(self)
        
        # Setup popup
        self.prompt = Prompt(self)
        
        self.set_view("editing")
        message = "Winston Churchill is widely regarded as one of the most effective leaders of the 20th century, particularly for his leadership during World War Il. However, what made Churchill's leadership style so successful? One way to answer this question is by"
        self.view_list["editing"].text_frame.text.set(message)
        message += "examining his leadership style through Blake and Mouton's Managerial Leadership Grid. The Managerial Leadership Grid is a tool that assesses a leader's concern for task completion and concern for people, resulting in five leadership styles: impoverished, country club, middle-of-the-road, team, and authority-compliance. Based on his actions and behaviors during World War Il, it is likely that Churchill's leadership style falls under the authority-compliance category of the Grid. This style is characterized by a high"
        self.view_list["editing"].text_frame.text.set(message)
        message += "concern for task completion and a low concern for people. Despite its limitations, Churchill's authority-compliance leadership style proved highly effective during the war. He was able to rally the British people and coordinate the country's war efforts, ultimately leading to victory over Nazi Germany. However, this style also had its drawbacks, such as the strain it put on Churchill's relationships with his"
        self.view_list["editing"].text_frame.text.set(message)
        message += "subordinates and the potential for burnout. While Churchill's leadership style may not be suitable for all contexts, it provides valuable insights into the complex interplay between task completion and concern for people in leadership. By using the Managerial Leadership Grid to analyze Churchill's leadership style, we can learn from his successes and limitations and apply these lessons to"
        self.view_list["editing"].text_frame.text.set(message)
        message += "subordinates and the potential for burnout. While Churchill's leadership style may not be suitable for all contexts, it provides valuable insights into the complex interplay between task completion and concern for people in leadership. By using the Managerial Leadership Grid to analyze Churchill's leadership style, we can learn from his successes and limitations and apply these lessons to"
        self.view_list["editing"].text_frame.text.set(message)
        message += "contemporary leadership development. In conclusion, Winston Churchill's leadership during World War II exemplifies the authority-compliance leadership style as identified by Blake and Mouton's Managerial Leadership Grid. While this style may not be appropriate for all situations, it proved highly effective in rallying a country and leading it to victory. By examining Churchill's leadership style through the Grid, we can gain valuable insights into the role of task completion and concern for people in effective leadership, and apply these lessons to contemporary"
        self.view_list["editing"].text_frame.text.set(message)
        """
        organizational contexts.)"""
        
        self.mainloop()
        
    def set_view(self, pointer: str):
        try:
            self.view_list[pointer].tkraise()
        except KeyError:
            raise ValueError(f"Unknown view '{pointer}'")
        
    def edit(self, option: str, output: ctk.StringVar):
        self.prompt.text_frame.text.set(output.get())
        self.prompt.show()
    #     if option in enhancements_prompts.keys():
    #         prompt = enhancements_prompts[option]
    #         edit = "enhance"
    #     elif option in suggestion_prompts.keys():
    #         prompt = suggestion_prompts[option]
    #         edit = "suggest"
    #     message = output.get()
    #     total_input = f"{prompt}\n\n{message}"
        
    #     if message and option:
    #         self.messages.append({"role": "user", "content": total_input})
    #         chat = client.chat.completions.create(model="gpt-3.5-turbo", 
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": total_input
    #             }
    #         ], 
    #         max_tokens=1000) 
    #         reply = chat.choices[0].message.content
            
    #         if edit == "enhance":
    #             output.set(reply)
    #         elif edit == "suggest":
    #             self.prompt.text_frame.text.set(reply)
    #             self.prompt.show()