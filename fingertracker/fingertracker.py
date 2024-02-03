import math
import threading

from pynput.mouse import Controller, Button

from recorder import HandRecorder
from recorder import HandLandmarkerResult 

class FingerTracker:
    """
    A controller that stimulates mouse movement using the direction of a pointed finger.
    """
    KEYPOINTS = {"index":(5, 8)}
    
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
        self.previous_coords = (0, 0)
        self.current_coords = (0, 0)
        self.disable_click = False
        
    def init(self):
        """Initialize timer and turn on camera"""
        self.recorder.start_camera()
        self.timer = threading.Timer(2, self.click)
        
    def _get_finger_direction(self, landmarks: HandLandmarkerResult, keypoints: tuple[int, int]):
        """
        Calculate and return the normalized coordinates on screen corresponding to a user's point

        Args:
            landmarks (HandLandmarkerResult): a mediapipe handlandmarker result object
            keypoints (tuple[int, int]): a tuple with integers corresponding to the indices of the finger joints

        Returns:
            float: an (x, y) coordinate pair of normalized corrdinates corresponding to the user's pointed index finger
        """
        # Get joint coordinates
        a = [landmarks[keypoints[0]].x, landmarks[keypoints[0]].y, abs(landmarks[0].z)-landmarks[keypoints[0]].z]
        b = [landmarks[keypoints[1]].x, landmarks[keypoints[1]].y, abs(landmarks[0].z)-landmarks[keypoints[1]].z]
        
        # Get corresponding screen coordinates
        slope = (b[0]-a[0])/(b[2]-a[2])
        x_coord = slope * (0.3 - a[2]) + a[0]
        
        slope = (b[1]-a[1])/(b[2]-a[2])
        y_coord = slope * (0.3 - a[2]) + a[1]
        
        # Constrain coordinates to normalized range
        if x_coord > 1:
            x_coord = 1
        elif x_coord < 0:
            x_coord = 0

        if y_coord < 0:
            y_coord = 0
        elif y_coord > 1:
            y_coord = 1
            
        # Create deadzone for more consistent tracking
        if math.dist((x_coord, y_coord), self.current_coords) < 0.05:
            x_coord = self.current_coords[0]
            y_coord = self.current_coords[1]
            
            # If user points at a spot for a certain time, click the location
            if not self.timer.is_alive():
                self.timer = threading.Timer(1.25, self.click)
                self.timer.start()
        else:
            # If user moves from the spot, do not click
            if self.timer.is_alive():
                self.timer.cancel()

        self.current_coords = (x_coord, y_coord)
        
        return self.current_coords
    
    def get_screen_coords(self):
        """
        Return the unnormalized location on screen an index finger is pointing at

        Returns:
            tuple[int, int]: an (x, y) coordinate pair representing where on screen the user is pointing
        """
        results = self.recorder.run()
        if results != None:
            normalized_coords = self._get_finger_direction(results, self.KEYPOINTS["index"])
            x = normalized_coords[0]*self.screen_size[0]
            y = normalized_coords[1]*self.screen_size[1]

            return (x, y)

    def move_cursor(self):
        """Move the cursor to the location indicated by index finger"""
        # TODO: Test offset with mirror
        coords = self.get_screen_coords()
        if coords != None:
            # Calculate velocity
            x_dist = coords[0] - self.controller.position[0]
            y_dist = coords[1] - self.controller.position[1]
            scalar = 0.1   # Velocity multiplier
            velocity = (x_dist*scalar, y_dist*scalar)
            
            # Update cursor location
            position = (self.controller.position[0]+velocity[0], self.controller.position[1]+velocity[1])
            self.controller.position = position
            
    def click(self):
        """Click the screen at the current cursor location"""
        if self.disable_click == False:
            self.controller.click(Button.left)