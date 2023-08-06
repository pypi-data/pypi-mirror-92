import pyttsx3
from gtts import gTTS
import speech_recognition as sr
from speech_recognition import Recognizer
class LS_Convert:



    def __init__(self):
        self.config = {
            "microphone_index": 1,
            "language": "ru-RU",
            "pause": 1,
            "record alert": False
        }

        self.__engine__ = pyttsx3.init()
        self.__engine__.setProperty('voice',self.config["language"])

        self.r = Recognizer()
        self.m = sr.Microphone()



    def say(self, text):
        self.__engine__.say(text)
        self.__engine__.runAndWait()


    def read_text(self, file):
        with open(file, "r") as file:
            file = file.read()
        self.__engine__.say(file)
        self.__engine__.runAndWait()


    def listen(self):
        self.m.device_index = self.config['microphone_index']
        with self.m as source:
            self.r.pause_threshold = self.config['pause']
            if self.config["record alert"] == True:
                print("Record")
            try:
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.listen(source)
                text = self.r.recognize_google(audio, language=self.config["language"])
                return text
            except:
                pass

