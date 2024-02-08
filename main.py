import tkinter as tk
import customtkinter as ctk
from openai import OpenAI

client = OpenAI()

from presenterai.app import App
from fingertracker.fingertracker import FingerTracker

# finger_tracker = FingerTracker((1440, 900))
# finger_tracker.init()

# while True:
#     finger_tracker.move_cursor()

"""prompt = "Can you edit my essay?"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role":"user",
            "content":prompt
        }
    ],
    model="gpt-3.5-turbo"
)

print(chat_completion)"""
App()