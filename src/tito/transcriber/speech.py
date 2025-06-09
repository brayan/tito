import subprocess

def speak(text: str):
    try:
        subprocess.run(["say", text])
    except Exception as e:
        print(f"TTS error: {e}")
