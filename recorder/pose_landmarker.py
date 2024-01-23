import math
import os
import time

import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from PIL import Image, ImageTk
import tkinter

from recorder.util.recorder import Recorder

mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles 
mp_pose = mp.solutions.pose

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult

previous_time = time.time()
# TODO: Add sanity checker for detections
# TODO: Remove live video output
# TODO: Save video to drive
class PoseRecorder(Recorder):
    def __init__(self, dst: tkinter.Canvas = None, output_size=(256, 256)):
        self._dst = dst
        super().__init__(os.path.join("recorder", "models", "pose_landmarker_lite.task"), output_size)
        
    def _init_detector(self) -> PoseLandmarker:
        """Create and return pose landmarker"""
        return PoseLandmarker.create_from_options(PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model),
            min_pose_detection_confidence=0.6,
            min_pose_presence_confidence=0.6,
            min_tracking_confidence=0.6,
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self._data_handler)
        )
        
    def _data_handler(self, result: PoseLandmarkerResult, image: mp.Image, timestamp: int) -> None:
        """Wrapper function for parent handler"""
        global previous_time
        super()._data_handler(result, image, timestamp)
        current_time = time.time()
        fps = 1/(current_time-previous_time)
        previous_time = current_time
        #print(fps)
            
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
            
    def get_angle(self, landmarks, keypoints) -> int:
        """
        Calculate and return middle angle of keypoints

        Returns:
            angle (int): angle of inner elbow in degrees. -1 if no angle found. [0, 180] otherwise.
        """
        # Determine visible joints
        joints = [keypoints[0], keypoints[1], keypoints[2]]
        visible = [landmarks[joint].visibility > 0.5 for joint in joints]
        
        if all(visible):
            # Get joint coordinates
            a = [landmarks[keypoints[0]].x, landmarks[keypoints[0]].y]
            b = [landmarks[keypoints[1]].x, landmarks[keypoints[1]].y]
            c = [landmarks[keypoints[2]].x, landmarks[keypoints[2]].y]
            
            # Get distances of joints
            a_to_b = math.dist(a, b)
            b_to_c = math.dist(b, c)
            c_to_a = math.dist(c, a)
            
            # Use law of cosines to get angle and convert to degrees
            radians = math.acos(
                (c_to_a**2 - (a_to_b**2 + b_to_c**2))/(-2*a_to_b*b_to_c)
                )
            angle = abs(radians*180/math.pi)
        else:
            return -1
                
        return angle
            
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
        
        if self._current_result != None and self._current_result.pose_landmarks:
            return self._current_result.pose_landmarks[0]
        else:
            return None