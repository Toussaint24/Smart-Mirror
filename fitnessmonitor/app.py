import sys

from tkinter import Tk

from fitnessmonitor.exercise import curl
import fitnessmonitor.views as views
from recorder.pose_landmarker import PoseRecorder

joint_keypoint_dict = {
    "elbow_left": (12, 14, 16),
    "elbow_right": (11, 13, 15),
    "shoulder_left": (24, 12, 14),
    "shoulder_right": (23, 11, 13)
}

class App:
    
    def __init__(self, root: Tk):
        self.root = root
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1) 
        self._init_views()
        self.position = 1
        self.counter = 0
        
    def _init_views(self):
        self._main_view = views.MainView(self.root, self)
        self._settings_view = views.SettingsView(self.root, self)
        self._exercises_view = views.ExerciseListView(self.root, self)
        self._recorder_view = views.RecorderView(self.root, self)
        
        self.view_list = views.View.view_list
        
        self.set_view("main")
        
    def set_view(self, pointer: str):
        self.view_list[pointer].tkraise()
        
    def run_exercise(self):
        joint = "elbow_right"
        data = self._recorder.run()
        if data != None:
            angle = self._recorder.get_angle(data, joint_keypoint_dict[joint])
            dict_ = {joint: angle}
            if angle == -1:
                angle = 80
            result = curl.process(self.position, dict_)
            if result[0] == True:
                if self.position == 1:
                    self.position = 0
                    self.counter += 1
                    print("Up")
                else:
                    self.position = 1
                    print("Down")
        if self._recorder._running:
            self._recorder_view.after(1, self.run_exercise)
        
    def record(self):
        self.current_exercise = curl.name
        self.set_view("recorder")
        self._recorder = PoseRecorder(
                dst=self._recorder_view.display, 
                output_size=(self.root.winfo_screenwidth(), 
                             self.root.winfo_screenheight())
        )
        self._recorder.start_camera()
        self.run_exercise()
        
    def stop_recording(self):
        self._recorder.close()
        self.set_view("main")

    def quit(self):
        if self._recorder._running():
            self.stop_recording()
        sys.exit()