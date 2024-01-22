import sys

from tkinter import Tk

from recorder.pose_landmarker import PoseRecorder
import fitnessmonitor.views as views


class App:
    
    def __init__(self, root: Tk):
        self.root = root
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1) 
        self._initViews()
        
    def _initViews(self):
        self._main_view = views.MainView(self.root, self)
        self._settings_view = views.SettingsView(self.root, self)
        self._exercises_view = views.ExerciseListView(self.root, self)
        self._recorder_view = views.RecorderView(self.root, self)
        
        self._setView(self._main_view)
        
    def _setView(self, view: views.View):
        view.tkraise()
        self._current_view = view
        
    def update(self, request: str):
        if self._current_view == self._main_view:
            
            if request == "exer_list":
                self._setView(self._exercises_view)
            elif request == "settings":
                self._setView(self._settings_view)
            elif request == "quit":
                self._quit()
            
        elif self._current_view == self._settings_view:
            
            pass
        
        elif self._current_view == self._exercises_view:
            
            if request == "Lorem":
                print("Here")
                self._setView(self._recorder_view)
                self._record()
            elif request == "back":
                self._stop_recording()
                self._setView(self._main_view)
        
    def _record(self):
        # Remove threading from recorders
        # Add if running condition to after method in recorder
        # Display image in canvas rather than label
        self._recorder = PoseRecorder(
                dst=self._recorder_view.display, 
                output_size=(self.root.winfo_screenwidth(), 
                             self.root.winfo_screenheight())
                )
        self._recorder.run()
        
    def _stop_recording(self):
        self._recorder.close()

    def _quit(self):
        if self._recorder.is_alive():
            self._stop_recording()
        sys.exit()