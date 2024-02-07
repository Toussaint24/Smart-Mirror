import sys
import threading
import time

from tkinter import Tk
import customtkinter as ctk

from fitnessmonitor.exercise import curl
from fitnessmonitor.views import *
from recorder import PoseRecorder

joint_keypoint_dict = {
    "elbow_left": (12, 14, 16),
    "elbow_right": (11, 13, 15),
    "shoulder_left": (24, 12, 14),
    "shoulder_right": (23, 11, 13)
}

class App(ctk.CTk):
    view_list = {}
    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__(fg_color="black")
        self.attributes("-fullscreen", True)
        self.overrideredirect(True)
        self.resizable(False, False)
        
        self._recorder = PoseRecorder(
                output_size=(self.winfo_screenwidth(), self.winfo_screenheight())
        )
        self._timer = threading.Timer(5, self.stop_recording)

        self.position = ctk.IntVar(value=0)
        self.position_str = ctk.StringVar(value="Direction:\ndown")
        self.counter = ctk.StringVar(value="Reps:\n0")
        self.message = ctk.StringVar(value="")
        
        self.in_position = False
        
        Main(self)
        Settings(self)
        ExerciseList(self)
        Recorder(self)
        
        self.set_view("main")
        self.mainloop()
        print("Here")
        
    def set_view(self, pointer: str):
        self.view_list[pointer].tkraise()
        
    def update_counter(self):
        counter_message = self.counter.get()
        counter_message = counter_message.replace(counter_message[-1], str(int(counter_message[-1])+1))
        self.counter.set(counter_message)      
        
    def update_position(self):
        if "down" in self.position_str.get():
            self.position.set(1)
            self.position_str.set("Direction:\nup")
            if self.in_position:
                self.update_counter()
        else:
            self.position.set(0)
            self.position_str.set("Direction:\ndown")
            
    def update_timer(self, cancel: bool = False):
        if cancel:
            # User found: Cancel inactivity timer
            if self._timer.is_alive():
                self.message.set("")
                self._timer.cancel()
        else:
            # User not found: Begin inactivity timer
            if not self._timer.is_alive():
                self.message.set("Status:\nNo user detected. Closing.")
                self._timer = threading.Timer(5, self.stop_recording)
                self._timer.start()
        
    def run_exercise(self):
        joint = "elbow_right"
        user_found = False # Boolean flag for inactivity timer
        data = self._recorder.run()
        
        if data != None:
            user_found = True
            
            # Get angle
            angle = self._recorder.get_angle(data, joint_keypoint_dict[joint])

            if angle != None:
                primary_flag, constraint_flag = curl.process(self.position.get(), {joint: angle})
                
                if primary_flag == True:
                    self.update_position()
                    self.in_position = True
                    
                if curl.message != None:
                    self.message.set(f"Status:\n{curl.message}")
                    
        self.update_timer(user_found)
                
        if self._recorder._running:
            self.after(1, self.run_exercise)
        
    def record(self):
        self.current_exercise = curl.name
        self.set_view("recorder")
        self._recorder.start_camera()
        self.run_exercise()
        
    def stop_recording(self):
        self._recorder._running = False
        self.set_view("main")

    def quit(self):
        if self._recorder._running:
            self.stop_recording()
        sys.exit()