import math
import time

import cv2
import mediapipe as mp

HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult

class Recorder:
    def __init__(self, model: str, output_size: tuple[int, int]):
        self.model = model
        self.output_size = output_size
        self._current_frame = None
        self._current_result = None
        self._running = True
        self._DEBUG = False
        
    def _init_detector(self):
        """Create and return vision detector model"""
        raise NotImplementedError("method '_init_detector' was not overwritten in subclass")
    
    def _data_handler(self, result, image, timestamp):
        """Callback function for detector"""
        self._current_result = result
        
    def _draw_landmarks(self):
        raise NotImplementedError("method _draw_landmarks was not overwritten in subclass")
        
    def start_camera(self):
        self._cap = cv2.VideoCapture(0)
        self._detector = self._init_detector()
        self._running = True
        
    def visible(self, landmarks: HandLandmarkerResult | PoseLandmarkerResult, keypoints: tuple[int, ...]) -> tuple[int, ...]:
        return [landmarks[keypoint].visibility > 0.6 for keypoint in keypoints]
        
    def get_angle(self, landmarks: HandLandmarkerResult | PoseLandmarkerResult, keypoints: tuple[int, int, int]) -> int | None:
        """
        Calculate and return middle angle of keypoints
        
        Args:
            landmarks (HandLandmarkerResult | PoseLandmarkerResult): the landmark results.
            keypoints (int): a tuple of 3 indices corresponding to the relevant joints of the target angle.

        Returns:
            angle (int): angle of inner elbow in degrees. None if no angle found. [0, 180] otherwise.
        """
        # Determine visible joints
        joints = [keypoints[0], keypoints[1], keypoints[2]]
        visible = [landmarks[joint].visibility > 0.5 for joint in joints]
        
        if all(visible) or "hand_landmarker.task" in self.model: # Hand results have visibility of 0.0
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
            return None
                
        return angle
        
    def run(self) -> None:
        """Get camera feed and run hand landmarker"""
        # Get camera feed
        ret, frame = self._cap.read()
        
        if not self._running:
            self.close()
            return
        
        if ret == False:
            return
        
        # Image preprocessing
        frame = cv2.flip(frame, 1)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        
        # Detections
        timestamp = round(time.time()*1000)
        self._detector.detect_async(mp_image, timestamp)
        self._current_frame = frame
        
        if self._DEBUG:
            # Visualization
            if self._current_result != None:
                self._draw_landmarks() 
            
            """self._current_frame = cv2.resize(self._current_frame, (self.output_size[0], self.output_size[1]), 
                interpolation = cv2.INTER_LINEAR)"""
            
            cv2.imshow("Window", self._current_frame)
            
            if cv2.waitKey(1) == ord('q'):
                self.close()
    
    def close(self):
        try:
            self._cap.release()
        except AttributeError:
            pass
        else:
            cv2.destroyAllWindows()
        
        self._detector.close()