import math
import threading
import time

from pynput.mouse import Controller, Button

from recorder import HandRecorder
from recorder import HandLandmarkerResult

class FingerTracker:
    """
    A controller that stimulates mouse movement using the direction of a pointed finger.
    """
    KEYPOINTS = {"index":(5, 8),
                 "index_full":(5, 6, 7, 8)
                 }
    
    def __init__(self, screen_size: tuple[int, int] = (256, 256)):
        """
        Initialize a FingerTracker instance

        Args:
            screen_size (tuple[int, int], optional): a tuple representing the size of the screen in pixels. 
            (width, height). Defaults to (256, 256).
        """
        self.screen_size = screen_size
        self.recorder = HandRecorder(self.screen_size)
        self.controller = Controller()
        self.result = None
        self.disable_click = False
        
    def init(self):
        """Initialize timer and turn on camera"""
        self.recorder.start_camera()
        self.timer = threading.Timer(1, lambda: None)
        
    def _get_landmark_result(self) -> HandLandmarkerResult:
        return self.recorder.run()
    
    def _get_landmark_depth(self, origin, landmark) -> float:
        return abs(origin.z)-landmark.z
    
    def _get_finger_coords(self, keypoints, landmarks=None):
        if landmarks == None:
            landmarks = self._get_landmark_result()
        if landmarks == None:
            return None
        
        coords = []
        for i in range(len(keypoints)):
            landmark = landmarks[keypoints[i]]
            coords.append((landmark.x, landmark.y, self._get_landmark_depth(landmarks[0], landmark)))
            
        self.result = landmarks
            
        return tuple(coords)
    
    def _get_cross_section_coords(self, a: tuple[float, float, float], b: tuple[float, float, float], target: float):
        slope = (b[0]-a[0])/(b[2]-a[2])
        cross_x = slope * (target - a[2]) + a[0]
        
        slope = (b[1]-a[1])/(b[2]-a[2])
        cross_y = slope * (target - a[2]) + a[1]
        
        return (cross_x, cross_y)
    
    def _get_intercept(self, keypoints: tuple[int, int]) -> None | tuple[float, float]:
        try:
            a, b = self._get_finger_coords(keypoints)
        except TypeError:
            return
        
        # Get corresponding screen coordinates
        x_coord, y_coord = self._get_cross_section_coords(a, b, 0.3)

        # Constrain coordinates to normalized range
        if x_coord > 1:
            x_coord = 1
        elif x_coord < 0:
            x_coord = 0

        if y_coord < 0:
            y_coord = 0
        elif y_coord > 1:
            y_coord = 1
            
        # Get actualized screen coordinates
        x_coord *= self.screen_size[0]
        y_coord *= self.screen_size[1]
        
        return (x_coord, y_coord)
    
    def _pointing(self, landmarks):
        # Check to see if index finger keypoints are on a line
        # if finger tip depth is aligned with finger base, not pointing
        coords = self._get_finger_coords(self.KEYPOINTS["index_full"], landmarks)
        a = coords[0]
        b = coords[3]
        ERROR = 0.1
        
        expected_coords = []
        z = coords[1][2]
        expected_coords.append(self._get_cross_section_coords(a, b, z))
        z = coords[2][2]
        expected_coords.append(self._get_cross_section_coords(a, b, z))
        
        within_error = lambda a, b: True if math.dist(a, b) < ERROR else False

        if within_error(expected_coords[0], coords[1][0:2]) and within_error(expected_coords[1], coords[2][0:2]):
            return True
        else:
            return False
    
    def _in_deadzone(self, a: tuple[float, float], b: tuple[float, float]) -> None:
        if math.dist(a, b) < self.screen_size[0]*0.04:
            return True
        return False
        
    def move_cursor(self):
        """Move the cursor to the location indicated by index finger"""
        # TODO: Test offset with mirror
        previous_time = time.time()
        coords = self._get_intercept(self.KEYPOINTS["index"])
        if coords != None and self._pointing(self.result):

            if self._in_deadzone(coords, self.controller.position):
                if not self.timer.is_alive():
                    self.timer = threading.Timer(0.75, lambda: self.controller.click(Button.left))
                    self.timer.start()
                return
            else:
                if self.timer.is_alive():
                    self.timer.cancel()
            
            # Calculate velocity
            x_dist = coords[0] - self.controller.position[0]
            y_dist = coords[1] - self.controller.position[1]
            scalar = 0.1   # Velocity multiplier
            velocity = (x_dist*scalar, y_dist*scalar)
            
            # Update cursor location
            position = (self.controller.position[0]+velocity[0], self.controller.position[1]+velocity[1])
            self.controller.position = position
            
            fps = 1/(time.time()-previous_time)
            print(fps)