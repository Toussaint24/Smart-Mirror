import cv2

class Recorder:
    def __init__(self, model, output_size):
        self.model = model
        self.output_size = output_size
        self._detector = self._init_detector()
        self._current_frame = None
        self._current_result = None
        self._running = True
        
    def _init_detector(self):
        """Create and return vision detector model"""
        raise NotImplementedError("method '_init_detector' was not overwritten in subclass")
    
    def _data_handler(self, result, image, timestamp):
        """Callback function for detector"""
        self._current_result = result
        
    def start_camera(self):
        self._cap = cv2.VideoCapture(0)
        
    def run(self):
        raise NotImplementedError("method 'run' was not overwritten in subclass")
    
    def close(self):
        self._running = False
        self._cap.release()
        self._detector.close()