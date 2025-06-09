import os
from pathlib import Path

SAMPLE_RATE = 16000
WRAP_WIDTH = 100
MAX_CHARACTERS = 4000
LANGUAGE = "pt"
OUTPUT_DIR = Path("transcriptions")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
