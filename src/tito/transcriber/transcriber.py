import tempfile
import os
from pathlib import Path
from typing import Optional

import numpy as np
import whisper
from scipy.io.wavfile import write
from .config import SAMPLE_RATE, WRAP_WIDTH, LANGUAGE
from .speech import speak
from .utils import wrap_text

_model = None

def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("large")
    return _model

def transcribe_audio(audio_data: list[np.ndarray], output_path: Path) -> Optional[str]:
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            audio_np = np.concatenate(audio_data, axis=0)
            write(temp_audio.name, SAMPLE_RATE, audio_np)
            result = get_model().transcribe(
                temp_audio.name,
                # language=LANGUAGE,
                temperature=0,
                verbose=True
            )
            os.unlink(temp_audio.name)
        wrapped_text = wrap_text(result["text"], WRAP_WIDTH).strip()
        output_path.write_text(wrapped_text, encoding="utf-8")
        return wrapped_text
    except Exception as e:
        print(f"Transcription error: {e}")
        speak("An error occurred during transcription.")
        return None
