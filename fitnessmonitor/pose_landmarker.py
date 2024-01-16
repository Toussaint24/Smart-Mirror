import threading
import time

import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
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
VisionRunningMode = mp.tasks.vision.RunningMode

previous_time = time.time()
frames = 0

class Recorder(threading.Thread):
    def __init__(self, dst=None):
        self._dst = dst
        self._cap = cv2.VideoCapture(0)
        self._current_frame = None
        self._current_result = None
        self._running = True
        self._detector = self._init_detector()
        super().__init__()
        
    def _init_detector(self):
        return PoseLandmarker.create_from_options(PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self._data_handler)
        )
        
    def _calculate_framerate(self):
        global previous_time
        current_time = time.time()
        fps = 1/(current_time-previous_time)
        previous_time = current_time
        print(fps)    
        
    def _data_handler(self, result: PoseLandmarkerResult, image: mp.Image, timestamp: int):
        self._current_result = result
        if DEBUG:
            self._calculate_framerate()
            
    def _draw_landmarks(self):
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
    
    def run(self):
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