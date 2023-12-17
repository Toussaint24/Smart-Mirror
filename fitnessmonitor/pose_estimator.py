import mediapipe as mp
from PIL import Image, ImageTk
import cv2
from matplotlib import pyplot as plt
import numpy as np

mp_drawing = mp.solutions.drawing_utils


class Recorder:
    def __init__(self, cap=0, size=(256, 256), confidence_threshold=0.3):
        self.__cap = cv2.VideoCapture(cap)
        self._size = size
        self._confidence_threshold = confidence_threshold
        self.running = False
        self._initModel()
        
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
        
    def start(self, dst, flip=False):
        # Video capture loop
        self.running = True
        while self.running:
            # Initialize Webcam
            _, frame = self.__cap.read()
            frame = cv2.resize(frame, (960, 960))
            
            if flip:
                frame = cv2.flip(frame, 1)
                        
            # Resize image; must be multiples of 32
            img = frame.copy()
            img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 256,256)
            input_image = tf.cast(img, dtype=tf.int32)
            
            # Detection
            results = self._model(input_image)
            keypoints = results['output_0']
            
            # Visualization
            self._draw_connections(frame, keypoints, 0.3)
            self._draw_keypoints(frame, keypoints, 0.3)

            # Convert to Tk image for display
            blue, green, red = cv2.split(frame)
            img_tk = Image.fromarray(cv2.merge((red, green, blue)))
            img_tk = ImageTk.PhotoImage(image=img_tk)
            dst.configure(image=img_tk)
            dst.image = img_tk
                
        self._cap.release()
        
    def _initModel(self):
        # Download the model from TF Hub.
        model = hub.load("https://www.kaggle.com/models/google/movenet/frameworks/TensorFlow2/variations/singlepose-thunder/versions/4")
        movenet = model.signatures['serving_default']
        self._model = movenet
        self._EDGES = { # Defines connections between keypoints
            (0, 1): 'm',
            (0, 2): 'c',
            (1, 3): 'm',
            (2, 4): 'c',
            (0, 5): 'm',
            (0, 6): 'c',
            (5, 7): 'm',
            (7, 9): 'm',
            (6, 8): 'c',
            (8, 10): 'c',
            (5, 6): 'y',
            (5, 11): 'm',
            (6, 12): 'c',
            (11, 12): 'y',
            (11, 13): 'm',
            (13, 15): 'm',
            (12, 14): 'c',
            (14, 16): 'c'
    }
    
    def _draw_keypoints(self, frame, keypoints, confidence_threshold):
        # Unnmoralize coordinates
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
        
        # Draw sufficiently confident keypoints
        for kp in shaped:
            ky, kx, kp_conf = kp
            if kp_conf > confidence_threshold:
                cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)

    def _draw_connections(self, frame, keypoints, confidence_threshold):
        # Unnormalize coordinates
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
        
        for edge, color in self._EDGES.items():
            p1, p2 = edge
            y1, x1, c1 = shaped[p1]
            y2, x2, c2 = shaped[p2] #if start and end within 2 std devs?
            
            if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 3)