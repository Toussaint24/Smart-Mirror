import time

import cv2
import mediapipe as mp

class Recorder:
    def __init__(self, model: str, output_size: tuple[int, int]):
        self.model = model
        self.output_size = output_size
        self._detector = self._init_detector()
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
        
    def run(self) -> None:
        """Get camera feed and run hand landmarker"""
        # Get camera feed
        ret, frame = self._cap.read()
        
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
        self._running = False
        
        try:
            self._cap.release()
        except AttributeError:
            pass
        
        self._detector.close()