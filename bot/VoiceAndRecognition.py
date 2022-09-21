import json  # lavorare con file json e stringhe json
import os  # lavorare con il file system
import wave  # creare e leggere file audio wav

import speech_recognition  # riconoscimento vocale dell'utente (Speech-To-Text)
from vosk import Model, KaldiRecognizer  # riconoscimento offline

from utilities.Language import Language


class VoiceAndRecognition:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

    def __init__(self, name, sex, speech_language, recognition_language):
        self.name = name
        self.sex = sex
        self.speech_language = speech_language
        self.recognition_language = recognition_language

    def setup_bot_voice(self, tts_engine):
        voices = tts_engine.getProperty("voices")

        # settaggio lingua del bot
        if self.speech_language == Language.ITALIANO.value:
            tts_engine.setProperty("voice", voices[1].id)
        else:
            tts_engine.setProperty("voice", voices[2].id)

        # velocità del parlato del bot
        tts_engine.setProperty("rate", 150)

        return tts_engine

    def record_and_recognize_audio(self, microphone, recognizer, *args: tuple):
        with microphone:
            recognized_data = ""

            # regolazione del livello di rumore ambientale
            recognizer.adjust_for_ambient_noise(microphone, duration=2)

            # ascolto del comando
            try:
                print("In ascolto...")
                audio = recognizer.listen(microphone, timeout=50, phrase_time_limit=100)
                with open("./registrazione_audio.wav ", "wb") as file:
                    file.write(audio.get_wav_data())
            except speech_recognition.WaitTimeoutError:
                print("Controllare se il microfono è acceso, per favore.")
                return

            # utilizzo del riconoscimento online tramite Google
            try:
                print("Inizio del riconoscimento vocale... ")
                if self.recognition_language == Language.ITALIANO.value:
                    recognized_data = recognizer.recognize_google(audio, language=Language.ITALIANO.value).lower()
                else:
                    recognized_data = recognizer.recognize_google(audio, language=Language.INGLESE.value).lower()
            except speech_recognition.UnknownValueError:
                print("Riprova.")
                pass
            # in caso di problemi con l'accesso a Internet, cercando di utilizzare il riconoscimento vocale offline
            except speech_recognition.RequestError:
                print("Cerco di utilizzare il riconoscimento vocale offline...")
                recognized_data = self.use_offline_recognition()

            os.remove("./registrazione_audio.wav ")

            return recognized_data

    def use_offline_recognition(self):
        recognized_data = ""
        try:
            # verifica dell'esistenza di un modello nella lingua richiesta nella directory dell'applicazione
            if not os.path.exists("../models/modello_italiano"):
                print("Scaricare il modello da:\n"
                      "https://alphacephei.com/vosk/models e decomprimere nella cartella models.")
                exit(1)

            # estrazione dell'audio registrato nel microfono
            audio_file = wave.open("./registrazione_audio.wav ", "rb ")
            data = audio_file.readframes(audio_file.getnframes())

            # settaggio del riconoscimento offline
            if self.recognition_language == Language.ITALIANO.value:
                model = Model("../models/modello_italiano")
            else:
                model = Model("../models/modello_inglese")
            offline_recognizer = KaldiRecognizer(model, audio_file.getframerate())

            # interpretazione del comando
            if len(data) > 0:
                if offline_recognizer.AcceptWaveform(data):
                    # ottenere i dati di testo riconosciuti dalla stringa JSON
                    recognized_data = offline_recognizer.Result()
                    recognized_data = json.loads(recognized_data)
                    recognized_data = recognized_data["text"]
        except ():
            print("Mi spiace, il servizio non è attualmente disponibile. Riprovare più tardi.")

        return recognized_data

    @staticmethod
    def play_voice_bot_speech(tts_engine, text_to_speech):
        tts_engine.say(str(text_to_speech))
        tts_engine.runAndWait()
