import os
from pathlib import Path

SAMPLE_RATE = 16000
WRAP_WIDTH = 100
MAX_CHARACTERS = 4000
LANGUAGE = "en"
OUTPUT_DIR = Path("transcriptions")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
