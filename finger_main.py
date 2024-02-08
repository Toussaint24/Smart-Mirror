import pyautogui
from fingertracker.fingertracker import FingerTracker

finger_tracker = FingerTracker(pyautogui.size())
finger_tracker.init()

while True:
    finger_tracker.move_cursor()