import sys
import threading

from tkinter.ttk import Button, Label
from tkinter import Tk, StringVar, Image

from pose_estimator import Recorder
import views


class App:
    
    def __init__(self):
        self._initViews()
        self._recorder = Recorder()
        self._recording_thread = threading.Thread(
            target=lambda: self._recorder.start(self._recorder_view.display, True), daemon=True
            )
        
    def _initViews(self):
        self._main_view = views.MainView(root, self)
        self._settings_view = views.SettingsView(root, self)
        self._exercises_view = views.ExerciseListView(root, self)
        self._recorder_view = views.RecorderView(root, self)
        
        self._main_view.pack(expand=1, fill="both")
        self._current_view = self._main_view
        
    def _setView(self, view):
        self._current_view.forget()
        self._current_view = view
        self._current_view.pack(expand=1, fill="both")
        
    def update(self, request):
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
                self._record()
                self._setView(self._recorder_view)
            elif request == "back":
                self._stop_recording()
                self._setView(self._main_view)
        
    def _record(self):
        if not self._recording_thread.is_alive():
            self._recording_thread.start()
        
    def _stop_recording(self):
        self._recorder.running = False
        self._recording_thread.join()

    def _quit(self):
        if self._recording_thread.is_alive():
            self._stop_recording()
        sys.exit()
                
    
if __name__ == "__main__":
    root = Tk()
    root.attributes("-fullscreen", True)
    app = App()
    root.mainloop()
