from functools import partial
from typing import Callable
import os
import sys
import threading

from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget)

import constants
import views
import models

class Frame:
    def __init__(self, view: views.View, model: Callable[[], None] = None):
        self._view = view
        self._model = model
        self._frame = {"model":self._model, "view":self._view}
        
    def __getitem__(self, key):
        return self._frame[key]

class FitnessMonitor(QMainWindow):
    def __init__(self, size):
        super().__init__()
        self.setFixedSize(size)
        self._currentExercise = None
        self._initFrames()
        self.recordingThread = threading.Thread(target=self._recorderFrame["model"].func, daemon=True)
        
    def _initFrames(self):
        self._mainFrame = Frame(view=views.MainView(self))
        
        view = views.ExerciseListView(self)
        self._exerListFrame = Frame(view, self._switchFrames)
        
        view = views.RecorderView(self)
        self._recorderFrame = Frame(view, models.RecorderModel(view))
        
        self._connectSignalsAndSlots()
        self._currentFrame = self._mainFrame
        self._exerListFrame["view"].hide()
        self._recorderFrame["view"].hide()
        self.setCentralWidget(self._mainFrame["view"])
        
    def _switchFrames(self, frame):
        self._currentFrame["view"].hide()
        self._currentFrame = frame
        self.setCentralWidget(frame["view"])
        frame["view"].show()
        
    def _connectSignalsAndSlots(self):
        frame = self._mainFrame
        frame["view"].button.clicked.connect(partial(self._switchFrames, self._exerListFrame))
        
        frame = self._exerListFrame
        frame["view"].button.clicked.connect(partial(self._startExercise, self._recorderFrame))
        
        frame = self._recorderFrame
        frame["view"].button.clicked.connect(self._record)
        
    def _startExercise(self, frame):
        self._switchFrames(frame)
        self._record()
        
    def _record(self):
        # Check for if thread is already running
        self.recordingThread.start()

    def _calibrate(self):
        pass
    
    def close(self):
        self._recorderFrame["model"].running = False
        self.recordingThread.join()
        super().close()
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    print(screen.size())
    window = FitnessMonitor(screen.size())
    window.showFullScreen() # Enable full screen
    sys.exit(app.exec())
