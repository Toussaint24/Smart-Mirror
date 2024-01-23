import math
import os
import time

import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

from .util.recorder import Recorder

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles 

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult

previous_time = time.time()

class HandRecorder(Recorder):
    def __init__(self, output_size=(256, 256)):
        super().__init__(os.path.join("recorder", "models", "hand_landmarker.task"), output_size)

    def _init_detector(self) -> HandLandmarker:
        """Create and return hand landmarker"""
        return HandLandmarker.create_from_options(HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model),
            num_hands=2,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7,
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self._data_handler)
        )
        
    def _data_handler(self, result: HandLandmarkerResult, image: mp.Image, timestamp: int) -> None:
        """Wrapper function for parent handler"""
        global previous_time
        super()._data_handler(result, image, timestamp)
        current_time = time.time()
        fps = 1/(current_time-previous_time)
        previous_time = current_time
        #print(fps)
        
    def _pointing(self):
        pass
        
    def _draw_landmarks(self) -> None:
        """Draws pose landmarks and connections"""
        for landmarks in self._current_result.hand_landmarks:
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in landmarks
            ])
            mp_drawing.draw_landmarks(
                self._current_frame,
                hand_landmarks_proto,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style())
            
    def run(self) -> None:
        """Get camera feed and run pose landmarker"""
        # Get camera feed
        _, frame = self._cap.read()
        
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
        
        """self._current_frame = cv2.resize(self._current_frame, (self.output_size[0], self.output_size[1]), 
               interpolation = cv2.INTER_LINEAR)"""
        
        cv2.imshow("Window", self._current_frame)
        
        if len(self._current_result.handedness) > 0:
            handedness_results = self._current_result.handedness[0]
            
            # Determine which hand in list is right hand
            handedness_index = -1
            for i in range(len(handedness_results)):
                if handedness_results[i].category_name == "Left": # Computer vision is flipped
                    handedness_index = i

            if handedness_index != -1:
                hand_result = self._current_result.hand_landmarks[handedness_index]
                return hand_result
            #print(self._get_finger_direction(hand_result, (5, 8)))
        
        return None