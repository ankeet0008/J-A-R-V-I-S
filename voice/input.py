try:
    import speech_recognition as sr
except Exception:
    sr = None
from config import WAKE_WORD
from utils.logger import info, debug

class VoiceInput:
    def __init__(self):
        self.recognizer = None
        self.microphone = None
        self.voice_mode = False

        if sr is None:
            info("SpeechRecognition is unavailable. Falling back to text input mode.")
            return

        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            with self.microphone as source:
                info("Calibrating microphone for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                info("Calibration complete.")
            self.voice_mode = True
        except Exception as e:
            info(f"Microphone initialization failed ({e}). Falling back to text input mode.")

    def listen_for_wake_word(self):
        """Listens continuously until the wake word is detected."""
        if not self.voice_mode:
            text = input(f"Type '{WAKE_WORD}' to wake Jarvis: ").strip().lower()
            return WAKE_WORD in text

        print(f"Listening for wake word: '{WAKE_WORD}'...")
        while True:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, phrase_time_limit=3)
                    
                text = self.recognizer.recognize_google(audio).lower()
                debug(f"Heard during wake search: {text}")
                
                if WAKE_WORD in text:
                    return True
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                debug(f"Network error in speech recognition: {e}")
            except Exception as e:
                debug(f"Unexpected STT error: {e}")

    def listen_command(self):
        """Listens for the actual command after wake word."""
        if not self.voice_mode:
            text = input("You > ").strip()
            return text or None

        try:
            with self.microphone as source:
                print("Listening for command...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            text = self.recognizer.recognize_google(audio)
            info(f"User > {text}")
            return text
            
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
        except Exception:
            return None
