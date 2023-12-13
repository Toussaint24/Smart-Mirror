import os

import tensorflow as tf
import tensorflow_hub as hub
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PyQt6.QtGui import QPixmap, QImage

import views


class Model:
    def __init__(self, view):
        self._view = view
        
class RecorderModel(Model):
    EDGES = { # Defines connections between keypoints
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
    
    def __init__(self, view: views.RecorderView):
        super().__init__(view)
        self._cap = cv2.VideoCapture(0)
        self.running = False
        self.func = self.runPoseEstimation

    def runPoseEstimation(self):
        # Download the model from TF Hub.
        model = hub.load("https://www.kaggle.com/models/google/movenet/frameworks/TensorFlow2/variations/singlepose-thunder/versions/4")
        movenet = model.signatures['serving_default']

        def draw_keypoints(frame, keypoints, confidence_threshold):
            # Unnmoralize coordinates
            y, x, c = frame.shape
            shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
            
            # Draw sufficiently confident keypoints
            for kp in shaped:
                ky, kx, kp_conf = kp
                if kp_conf > confidence_threshold:
                    cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)

        def draw_connections(frame, keypoints, edges, confidence_threshold):
            # Unnormalize coordinates
            y, x, c = frame.shape
            shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
            
            for edge, color in edges.items():
                p1, p2 = edge
                y1, x1, c1 = shaped[p1]
                y2, x2, c2 = shaped[p2] #if start and end within 2 std devs?
                
                if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
                    cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 3)
                    
        self.running = True
        while self.running:
            # Initialize Webcam
            ret, frame = self._cap.read()
            frame = cv2.resize(frame, (960, 960))
            frame = cv2.flip(frame, 1)
                        
            # Resize image; must be multiples of 32
            img = frame.copy()
            img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 256,256)
            input_image = tf.cast(img, dtype=tf.int32)
            
            # Detection
            results = movenet(input_image)
            keypoints = results['output_0']
            
            # Visualization
            draw_connections(frame, keypoints, RecorderModel.EDGES, 0.3)
            draw_keypoints(frame, keypoints, 0.3)

            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QImage(frame.data, width, height, bytesPerLine, 
                          QImage.Format(13)).rgbSwapped().scaled(self._view.height(), self._view.height())

            self._view.label.setPixmap(QPixmap(qImg))
                
        self._cap.release()