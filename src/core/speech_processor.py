import speech_recognition as sr
import pyttsx3

class SpeechProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)

    def listen_for_command(self):
        """Listen for voice command"""
        with sr.Microphone() as source:
            print('🎤 Listening for command...')
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f'✅ Command received: {command}')
                return command
            except sr.WaitTimeoutError:
                print("⌛ Listening timed out. Try again.")
                return None
            except sr.UnknownValueError:
                print('❌ Sorry, I did not understand that.')
                return None
            except sr.RequestError as e:
                print(f'❌ Could not request results: {e}')
                return None

    def speak(self, text):
        """Speak the given text"""
        self.engine.say(text)
        self.engine.runAndWait()
