import json  # lavorare con file json e stringhe json
import os  # lavorare con il file system
import wave

import pyttsx3
import speech_recognition  # riconoscimento vocale dell'utente (Speech-To-Text)
from vosk import KaldiRecognizer  # riconoscimento offline

from utilities.Language import Language


class VoiceAndRecognition:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""
    tts_engine = pyttsx3.init()

    def __init__(self, name, sex, speech_language, recognition_language):
        self.name = name
        self.sex = sex
        self.speech_language = speech_language
        self.recognition_language = recognition_language
        self.setup_bot_voice()

    def setup_bot_voice(self):
        voices = self.tts_engine.getProperty("voices")

        # settaggio lingua del bot
        if self.speech_language == Language.ITALIANO.value:
            self.tts_engine.setProperty("voice", voices[1].id)
        else:
            self.tts_engine.setProperty("voice", voices[2].id)

        # velocità del parlato del bot
        self.tts_engine.setProperty("rate", 150)

    def use_recognition_online(self, microphone, recognizer_online, recognizer_offline):
        with microphone:
            recognized_data = ""

            # regolazione del livello di rumore ambientale
            recognizer_online.adjust_for_ambient_noise(microphone, duration=2)

            # ascolto del comando
            try:
                print("In ascolto...")
                audio = recognizer_online.listen(microphone, timeout=10, phrase_time_limit=20)
                with open("./registrazione_audio.wav", "wb") as file:
                    file.write(audio.get_wav_data())
            except speech_recognition.WaitTimeoutError:
                print("Controllare se il microfono è acceso, per favore.")
                return

            # utilizzo del riconoscimento online tramite Google
            try:
                print("Inizio del riconoscimento vocale...")
                if self.recognition_language == Language.ITALIANO.value:
                    recognized_data = recognizer_online.recognize_google(audio, language=Language.ITALIANO.value)
                else:
                    recognized_data = recognizer_online.recognize_google(audio, language=Language.INGLESE.value)
            except speech_recognition.UnknownValueError:
                print("Riprova.")
                pass
            # in caso di problemi con l'accesso a Internet, cercando di utilizzare il riconoscimento vocale offline
            except speech_recognition.RequestError:
                print("Cerco di utilizzare il riconoscimento vocale offline...")
                recognized_data = self.use_recognition_offline(recognizer_offline)

            os.remove("./registrazione_audio.wav")

            recognized_data = recognized_data.lower(). \
                replace("ì", "i'"). \
                replace("è", "e'"). \
                replace("é", "e'"). \
                replace("ò", "o'"). \
                replace("à", "a'"). \
                replace("ù", "u'")

            print("Tu: " + recognized_data)

            return recognized_data

    @staticmethod
    def use_recognition_offline(recognizer_offline):
        recognized_data = ""

        try:
            # estrazione dell'audio registrato nel microfono
            audio_file = wave.open("./registrazione_audio.wav", "rb")
            data = audio_file.readframes(audio_file.getnframes())

            recognizer_offline = KaldiRecognizer(recognizer_offline, audio_file.getframerate())

            # utilizzo del riconoscimento offline tramite Google
            if len(data) > 0:
                if recognizer_offline.AcceptWaveform(data):
                    # ottenere i dati di testo riconosciuti dalla stringa JSON
                    recognized_data = recognizer_offline.Result()
                    recognized_data = json.loads(recognized_data)
                    recognized_data = recognized_data["text"]
        except ():
            print("Mi spiace, il servizio non è attualmente disponibile. Riprovare più tardi.")

        recognized_data = recognized_data.lower(). \
            replace("ì", "i'"). \
            replace("è", "e'"). \
            replace("é", "e'"). \
            replace("ò", "o'"). \
            replace("à", "a'"). \
            replace("ù", "u'")

        print("Tu: " + recognized_data)

        return recognized_data

    def output_response(self, name_bot, bot_response):
        print(name_bot + ": " + str(bot_response))
        self.play_voice_bot_speech(bot_response)

    def play_voice_bot_speech(self, text_to_speech):
        self.tts_engine.say(str(text_to_speech))
        self.tts_engine.runAndWait()
