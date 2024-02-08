import math
import threading
import time

from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
from pynput.mouse import Controller, Button

from recorder import HandRecorder
from recorder import HandLandmarkerResult


class FingerTracker:
    """
    A controller that stimulates mouse movement using the direction of a pointed finger.
    """
    KEYPOINTS = {
        "index":(5, 8),
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
        self.CLICK_DEADZONE = 0.035*self.screen_size[0]
        self.MOVE_DEADZONE = 0.02*self.screen_size[0]
        
    def init(self):
        """Initialize timer and turn on camera"""
        self.recorder.start_camera()
        self.timer = threading.Timer(1, lambda: None)
        
    def _get_landmark_result(self) -> HandLandmarkerResult:
        """Return hand landmarks"""
        return self.recorder.run()
    
    def _get_landmark_depth(self, origin: NormalizedLandmark, landmark: NormalizedLandmark) -> float:
        """Return virtual depth of a landmark from the camera

        Args:
            origin (NormalizedLandmark): the reference landmark
            landmark (NormalizedLandmark): the target landmark

        Returns:
            float: the depth of the target landmark from the camera
        """
        return abs(origin.z)-landmark.z
    
    def _get_finger_coords(self, keypoints: tuple[int, ...], landmarks: HandLandmarkerResult | None = None):
        """Return the three-dimensional coordinates of the target finger as seen on the camera"""
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
        """Return the cross-sectional (x, y) of a target z coordinate on a line.

        Args:
            a (tuple[float, float, float]): a 3D coordinate point.
            b (tuple[float, float, float]): a 3D coordinate point.
            target (float): target z value to obtain the cross sectional coordinates at.

        Returns:
            tuple[float, float]: a coordinate pair representing the (x, y) coordinate pair where the line 
            intersects a cross-section.
        """
        slope = (b[0]-a[0])/(b[2]-a[2])
        cross_x = slope * (target - a[2]) + a[0]
        
        slope = (b[1]-a[1])/(b[2]-a[2])
        cross_y = slope * (target - a[2]) + a[1]
        
        return (cross_x, cross_y)
    
    def _get_intercept(self, keypoints: tuple[int, int]) -> None | tuple[float, float]:
        """Return the (x, y) screen coordinates of its intercept with the pointed finger.

        Args:
            keypoints (tuple[int, int]): a tuple containing the keypoint indices.

        Returns:
            None | tuple[float, float]: a tuple containing the unnormalized (x, y) screen coordinates or
            None if unavailable.
        """
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
    
    def _pointing(self):
        """Return a boolean value indicating if there is a user pointing at the camera.

        Args:
            landmarks (HandLandmarkerResult): the landmark results.

        Returns:
            bool: True if user is pointing at the camera
        """
        # Check to see if index finger keypoints are on a line
        # if finger tip depth is aligned with finger base, not pointing
        coords = self._get_finger_coords(self.KEYPOINTS["index_full"], self.result)
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
    
    def _in_deadzone(self, a: tuple[float, float], b: tuple[float, float], deadzone: float) -> None:
        """Return a boolean value indicating if the point is in the established deadzone.

        Args:
            a (tuple[float, float]): an (x, y) coordinate point
            b (tuple[float, float]): an (x, y) coordinate point

        Returns:
            bool: True if the point is outside the deadzone. Otherwise False.
        """
        if math.dist(a, b) < deadzone:
            return True
        return False
        
    def move_cursor(self):
        """Move the cursor to the location indicated by index finger"""
        # TODO: Test offset with mirror
        coords = self._get_intercept(self.KEYPOINTS["index"])

        if coords != None and self._pointing():

            if self._in_deadzone(coords, self.controller.position, self.CLICK_DEADZONE):
                if not self.timer.is_alive():
                    self.timer = threading.Timer(0.75, lambda: self.controller.click(Button.left))
                    self.timer.start()
            else:
                if self.timer.is_alive():
                    self.timer.cancel()
                    
            if self._in_deadzone(coords, self.controller.position, self.MOVE_DEADZONE):
                return
            
            # Calculate velocity
            x_dist = coords[0] - self.controller.position[0]
            y_dist = coords[1] - self.controller.position[1]
            scalar = 0.07   # Velocity multiplier
            velocity = (x_dist*scalar, y_dist*scalar)
            
            # Update cursor location
            position = (self.controller.position[0]+velocity[0], self.controller.position[1]+velocity[1])
            self.controller.position = position