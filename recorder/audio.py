import os
import time

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
from dotenv import load_dotenv
import pyaudio
import wave

load_dotenv()

API_KEY = os.getenv("DG_API_KEY")
FORMAT = pyaudio.paInt16
CHANNELS = 1
CHUNK = 1024


class AudioRecorder:
    def __init__(self, rate: int = 48000):
        self.rate = rate
        self.init_model()
        self.stopped = False
        self.paused = False
        
    def init_model(self):
        self.model = DeepgramClient(API_KEY)
        self.options = PrerecordedOptions(
            model="nova",
            smart_format=True,
            utterances=True,
            punctuate=True,
            paragraphs=True,
            filler_words=True,
        )
    
    def record(self):
        self.recorder = pyaudio.PyAudio()
        self.paused = False
        self.stopped = False
        self.stream = self.recorder.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=CHUNK)
        self.frames = []
        
        while not self.stopped:
            if not self.paused:
                data = self.stream.read(CHUNK)
                self.frames.append(data)
                
        self.close()
    
    def process(self):
        try:
            with open(self.filepath, "rb") as file:
                buffer_data = file.read()
            payload: FileSource = {
                "buffer": buffer_data,
            }
            response = self.model.listen.prerecorded.v("1").transcribe_file(payload, self.options)
            transcript = response["results"].channels[0].alternatives[0].paragraphs.transcript
            os.remove(self.filepath)
            return transcript
        
        except Exception as e:
            print("Exception:", e)
    
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.recorder.terminate()
        
        self.filepath = os.path.join("recorder", "temp", f"{time.time()}.wav")
        wf = wave.open(self.filepath, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.recorder.get_sample_size(FORMAT))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()