import toga
from toga.style import Pack
from toga.style.pack import COLUMN

import threading
import datetime
from pathlib import Path

from tito.transcriber.recorder import Recorder
from tito.transcriber.transcriber import transcribe_audio
from tito.transcriber.summarizer import generate_summary
from tito.transcriber.speech import speak
from tito.transcriber.utils import set_button_enabled
from tito.transcriber.utils import invoke_later
from tito.transcriber.notion_writer import send_transcription_to_notion

import logging
import traceback
from tito.utils.path import get_output_dir


class TitoApp(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.recorder = Recorder()
        self.recording_thread = None
        self.is_recording = False

        self.start_button = toga.Button(
            "Start Recording",
            on_press=self.start_recording,
            style=Pack(margin=5)
        )
        self.stop_button = toga.Button(
            "Stop and Transcribe",
            on_press=self.stop_and_transcribe,
            style=Pack(margin=5),
            enabled=False
        )
        self.status_label = toga.Label("Ready", style=Pack(margin=5))

        main_box.add(self.start_button)
        main_box.add(self.stop_button)
        main_box.add(self.status_label)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def start_recording(self, widget):
        self.update_status("Recording...")
        speak("Starting recording.")
        self.is_recording = True
        set_button_enabled(self, self.start_button, False)
        set_button_enabled(self, self.stop_button, True)

        self.recording_thread = threading.Thread(target=self._start_recording_thread)
        self.recording_thread.start()

    def _start_recording_thread(self):
        self.recorder.start()

    def stop_and_transcribe(self, widget):
        self.update_status("Stopping recording...")
        set_button_enabled(self, self.stop_button, False)

        try:
            self.recorder.stop()
            self.recording_thread.join()
            self.is_recording = False
            set_button_enabled(self, self.start_button, True)

            self.update_status("Processing transcription...")
            thread = threading.Thread(target=self._transcribe_and_summarize)
            thread.start()

        except Exception as e:
            self.handle_error("Error while stopping and starting transcription", e)

    def _transcribe_and_summarize(self):
        try:
            audio_data = self.recorder.audio
            if audio_data is None or len(audio_data) == 0:
                raise ValueError("No audio data available.")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_dir = get_output_dir() / "transcriptions"
            output_dir.mkdir(parents=True, exist_ok=True)
            transcript_file = output_dir / f"{timestamp}_session.txt"
            summary_file = output_dir / f"{timestamp}_summary.txt"

            self.update_status("Transcribing...")
            speak("Now transcribing.")
            transcription = transcribe_audio(audio_data, transcript_file)

            if not isinstance(transcription, str) or not transcription.strip():
                raise ValueError("Empty or invalid transcription.")

            self.update_status("Generating summary...")
            speak("Transcription saved. Generating summary.")
            summary = generate_summary(transcription, summary_file)

            if not summary.strip():
                logging.warning("Empty summary. Check the transcription or API response.")
                self.update_status("Empty summary.")
                speak("The summary could not be generated.")
                return

            summary_file.write_text(summary, encoding="utf-8")
            speak("Summary saved successfully.")
            self.update_status("Summary saved successfully.")

            speak("Sending to Notion.")
            send_transcription_to_notion(summary, context="Meeting")

        except Exception as e:
            self.handle_error("Error during transcription or summary", e)

    def update_status(self, message):
        def _update():
            invoke_later(lambda: setattr(self.status_label, "text", message))
        _update()

    def handle_error(self, message: str, exception: Exception):
        full_message = f"{message}: {exception}"
        self.update_status(f"Error: {exception}")
        speak("Unexpected error.")
        logging.error(full_message)
        logging.debug(traceback.format_exc())


def main():
    return TitoApp("Tito", "br.com.sailtech.tito")
