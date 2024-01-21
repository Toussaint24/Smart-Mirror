import threading
import time

import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import math
from PIL import Image, ImageTk

DEBUG = True

model_path = "fitnessmonitor/pose_landmarker_lite.task"

mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles 
mp_pose = mp.solutions.pose

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

previous_time = time.time()
frames = 0

# TODO: Add model_path parameter
# TODO: Remove live video output
# TODO: Save video to drive
class Recorder(threading.Thread):
    def __init__(self, dst=None):
        self._dst = dst
        self._cap = cv2.VideoCapture(0)
        self._current_frame = None
        self._current_result = None
        self._running = True
        self._detector = self._init_detector()
        super().__init__()
        
    def _init_detector(self) -> PoseLandmarker:
        """Create and return pose landmarker"""
        return PoseLandmarker.create_from_options(PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self._data_handler)
        )
        
    def _get_framerate(self) -> None:
        """Calculate current framerate"""
        global previous_time
        current_time = time.time()
        fps = 1/(current_time-previous_time)
        previous_time = current_time  
        
    def _data_handler(self, result: PoseLandmarkerResult, image: mp.Image, timestamp: int) -> None:
        """Callback function for detector"""
        self._current_result = result
        if DEBUG:
            self._get_framerate()
            
    def _draw_landmarks(self) -> None:
        """Draws pose landmarks and connections"""
        for landmarks in self._current_result.pose_landmarks:
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in landmarks
            ])
            mp_drawing.draw_landmarks(
                self._current_frame,
                pose_landmarks_proto,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing_styles.get_default_pose_landmarks_style())
            
    def get_arm_angle(self) -> int:
        """
        Calculate and return angle of inner elbow

        Returns:
            angle (int): angle of inner elbow in degrees. -1 if no angle found. [0, 180] otherwise.
        """
        
        # Check if results available
        try:
            landmarks = self._current_result.pose_landmarks[0]
        except:
            return -1
        
        # Determine visible joints
        pose_landmarks = mp_pose.PoseLandmark
        joints = [pose_landmarks.LEFT_SHOULDER, pose_landmarks.LEFT_ELBOW, pose_landmarks.LEFT_WRIST]
        visible = [landmarks[joint].visibility > 0.5 for joint in joints]
        
        if all(visible):
            # Get joint coordinates
            a = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
            b = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y]
            c = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y]
            
            # Get distances of joints
            shoulder_to_elbow = math.dist(a, b)
            elbow_to_wrist = math.dist(b, c)
            wrist_to_shoulder = math.dist(c, a)
            
            # Use law of cosines to get angle and convert to degrees
            radians = math.acos(
                (wrist_to_shoulder**2 - (shoulder_to_elbow**2 + elbow_to_wrist**2))/(-2*shoulder_to_elbow*elbow_to_wrist)
                )
            angle = abs(radians*180/math.pi)
        else:
            return -1
                
        return angle
            
    def run(self) -> None:
        """Get camera feed and run pose landmarker"""
        # Get camera feed
        ret, frame = self._cap.read()
        
        # Image preprocessing
        frame = cv2.flip(frame, 1)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        
        # Detections
        timestamp = round(time.time()*1000)
        self._detector.detect_async(mp_image, timestamp)
        self._current_frame = frame           
        
        # Visualization
        if self._current_result != None:
            self._draw_landmarks() 
            self.get_arm_angle()
        
        blue, green, red = cv2.split(self._current_frame)
        image_tk = Image.fromarray(cv2.merge((red, green, blue)))
        image_tk = ImageTk.PhotoImage(image=image_tk)
        self._dst.image = image_tk
        self._dst.configure(image=image_tk)
        
        self._dst.after(1, self.run)
            
    def close(self):
        self._running = False
        self._cap.release()
        self._detector.close()