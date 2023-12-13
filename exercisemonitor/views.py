from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget,  
    QLabel, 
    QLayout,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtGui import QPicture, QPixmap
import cv2


class View(QWidget):
    def __init__(self, parent: QWidget, size: tuple = None):
        super().__init__(parent)
        if size == None:
            self.resize(parent.width(), parent.height())
        else:
            self.resize(size[0], size[1])
  
        
class MainView(View):
    def __init__(self, parent: QWidget):
        super().__init__(parent, None)
        self.generalLayout = QVBoxLayout(self)
        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(self.generalLayout)
        self.button = QPushButton("Exercises", self)
        self.generalLayout.addWidget(self.button)
        
        
class ExerciseListView(View):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)
        self.button = QPushButton("Single Bicep Curls", self)
        self._layout.addWidget(self.button)
        
        
class RecorderView(View):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.centralWidget = QWidget()
        
        self.layout.addWidget(self.centralWidget)
        self.setLayout(self.layout)
        
        self.label = QLabel(self.centralWidget)
        self.label.resize(parent.height(), parent.height())
        self.label.move(self.rect().center().x()-(self.label.width()//2), 0)
        
        self.setStyleSheet("background-color: black; border:2px solid red;")
    
        self.button = QPushButton("Return", self.label)
        self.button.setFixedSize(50, 50)
        self.button.move(50, 50)
        self.button.setStyleSheet("background-color: white;")
        
        print(self.width(), self.height())
        print(self.label.width(), self.label.height())
