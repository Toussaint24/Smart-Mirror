import mediapipe as mp
from PIL import Image, ImageTk
import cv2
from matplotlib import pyplot as plt

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class Recorder:
    def __init__(self, cap=0, size=(256, 256), confidence_threshold=0.3):
        self.__cap = cv2.VideoCapture(cap)
        self._size = size
        self._confidence_threshold = confidence_threshold
        self.running = False
        
    def set_size(self, size):
        if type(size) == tuple:
            self._size = size
        else:
            raise TypeError("Size should be a tuple: (width, height)")
    
    def set_confidence_threshold(self, threshold):
        if type(threshold) == float or type(threshold) == int:
            if threshold >= 0 and threshold <= 1:
                self._confidence_threshold = threshold
            else:
                raise ValueError("Confidence threshold should be in the interval: 0>=val<=1")
        else:
            raise TypeError("Confidence threshold should be a numeric value")
        
    def start(self, size, dst, flip=False):
        # Video capture loop
        self.running = True
        with mp_pose.Pose(
            min_detection_confidence=self._confidence_threshold, 
            min_tracking_confidence=self._confidence_threshold
            ) as pose:
            while self.running:
                # Initialize Webcam
                _, frame = self.__cap.read()
                
                if flip:
                    frame = cv2.flip(frame, 1)
                
                # Recolor image
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                # Detection
                results = pose.process(image)
                
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                
                image = cv2.resize(image, (size[0], size[1]))

                # Convert to Tk image for display
                blue, green, red = cv2.split(image)
                img_tk = Image.fromarray(cv2.merge((red, green, blue)))
                img_tk = ImageTk.PhotoImage(image=img_tk)
                dst.configure(image=img_tk)
                dst.image = img_tk
                    
            self._cap.release()