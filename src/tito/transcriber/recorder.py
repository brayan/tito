import sounddevice as sd
import numpy as np
from threading import Event

class Recorder:
    def __init__(self, samplerate=16000):
        self.audio_data = []
        self.samplerate = samplerate
        self._stop_event = Event()
        self.audio = None

    def _callback(self, indata, frames, time, status):
        if self._stop_event.is_set():
            raise sd.CallbackStop
        self.audio_data.append(indata.copy())

    def start(self):
        self.audio_data.clear()
        self._stop_event.clear()
        self.audio = None
        self.stream = sd.InputStream(
            channels=1,
            samplerate=self.samplerate,
            callback=self._callback
        )
        self.stream.start()

    def stop(self):
        self._stop_event.set()
        self.stream.stop()
        self.stream.close()

        if self.audio_data:
            self.audio = np.concatenate(self.audio_data, axis=0)
        else:
            self.audio = None

        return self.audio
