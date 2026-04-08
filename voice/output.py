import pyttsx3
from config import TTS_ENGINE, VOICE_RATE

class VoiceOutput:
    def __init__(self):
        self.engine = None
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', VOICE_RATE)

            # Look for a masculine/system sounding voice
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if "male" in voice.name.lower() or "david" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        except Exception:
            self.engine = None
                
    def speak(self, text):
        print(f"Jarvis > {text}")
        if self.engine is not None:
            self.engine.say(text)
            self.engine.runAndWait()
