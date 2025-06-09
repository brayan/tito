import subprocess
import sys

def install_whisper_model():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "git+https://github.com/openai/whisper.git"])

if __name__ == "__main__":
    install_whisper_model()
