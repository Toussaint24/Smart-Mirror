import os

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

class HandRecorder(Recorder):
    def __init__(self, output_size: tuple[int, int] = (256, 256)):
        super().__init__(os.path.join("recorder", "models", "hand_landmarker.task"), output_size)

    def _init_detector(self) -> HandLandmarker:
        """Create and return hand landmarker"""
        return HandLandmarker.create_from_options(HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model),
            min_hand_detection_confidence=0.85,
            min_hand_presence_confidence=0.9,
            min_tracking_confidence=0.85,
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self._data_handler)
        )
        
    def _data_handler(self, result: HandLandmarkerResult, image: mp.Image, timestamp: int) -> None:
        """Wrapper function for parent handler"""
        super()._data_handler(result, image, timestamp)
        
    def _draw_landmarks(self) -> None:
        """Draws hand landmarks and connections"""
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
            
    def run(self) -> HandLandmarkerResult | None:
        """Get camera feed and run hand landmarker"""
        super().run()
        
        try:
            return self._current_result.hand_landmarks[0]
        except (AttributeError, IndexError):
            return None