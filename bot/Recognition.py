import json
import os
import wave

import speech_recognition
from vosk import KaldiRecognizer, Model

from utilities.Language import Language
from utilities.utils import DOWNLOAD_MODEL_ITA, DOWNLOAD_MODEL_ENG, normalize, MODEL_ITA, MODEL_ENG, REC_AUDIO, \
    CHECK_MICROPHONE_ENG, CHECK_MICROPHONE_ITA, VERIFIED_A_PROBLEM_ITA, VERIFIED_A_PROBLEM_ENG, LISTENING_ITA, \
    LISTENING_ENG, RECOGNITION_ITA, RECOGNITION_ENG


# noinspection PyShadowingNames
class Recognition:
    name_bot = ""
    language = ""
    recognizer_online = None
    recognizer_offline = None
    microphone = speech_recognition.Microphone()

    def __init__(self, name_bot, language):
        self.name_bot = name_bot
        self.language = language
        self.recognizer_online, self.recognizer_offline = self.setup_recognizers()

    def setup_recognizers(self):
        return self.init_recognizer_online(), self.init_recognizer_offline()

    @staticmethod
    def init_recognizer_online():
        return speech_recognition.Recognizer()

    def init_recognizer_offline(self):
        if self.language == Language.ITALIANO.value:
            if not os.path.exists(MODEL_ITA):
                print(DOWNLOAD_MODEL_ITA)
                exit(1)
            return Model(MODEL_ITA)
        else:
            if not os.path.exists(MODEL_ENG):
                print(DOWNLOAD_MODEL_ENG)
                exit(1)
            return Model(MODEL_ENG)

    def use_recognition_online(self, lan=None):
        with self.microphone:
            # regolazione del livello di rumore ambientale
            self.recognizer_online.adjust_for_ambient_noise(self.microphone, duration=2)

            # ascolto del comando
            try:
                print(LISTENING_ITA) if self.language == Language.ITALIANO.value else print(LISTENING_ENG)

                # estrai audio dal microfono
                audio = self.recognizer_online.listen(self.microphone)

            # nessun audio rilevato durante il time out
            except lan.WaitTimeoutError:
                return False, CHECK_MICROPHONE_ITA \
                    if self.language == Language.ITALIANO.value \
                    else False, CHECK_MICROPHONE_ENG

            # utilizzo del riconoscimento online
            try:
                print(RECOGNITION_ITA) if self.language == Language.ITALIANO.value else print(RECOGNITION_ENG)

                # estrazione stringa dal comando vocale
                recognized_data = self.recognizer_online.recognize_google(audio, language=Language.ITALIANO.value) \
                    if self.language == Language.ITALIANO.value else \
                    self.recognizer_online.recognize_google(audio, language=Language.INGLESE.value)

            # riconoscimento online fallito
            except speech_recognition.UnknownValueError:
                return False, None

            # problemi con l'accesso a Internet

            except speech_recognition.RequestError:
                # salva audio in caso di riconoscimento offline
                with open(REC_AUDIO, "wb") as file:
                    file.write(audio.get_wav_data())
                recognized_data = self.use_recognition_offline()

            # rimozione audio salvato
            os.remove(REC_AUDIO)

            # normalizzazione maiuscole e accenti
            recognized_data = normalize(recognized_data)

            # ritorno stringa del comando vocale
            print("Tu: " + recognized_data)
            return True, recognized_data

    def use_recognition_offline(self):
        def extract_test_from():
            recognized_data = recognizer_offline.Result()
            recognized_data = json.loads(recognized_data)
            return recognized_data["text"]

        recognized_data = ""
        try:
            # estrazione audio salvato
            audio_file = wave.open(REC_AUDIO, "rb")
            data = audio_file.readframes(audio_file.getnframes())

            # utilizzo del riconoscimento offline
            recognizer_offline = KaldiRecognizer(self.recognizer_offline, audio_file.getframerate())
            if len(data) > 0:
                if recognizer_offline.AcceptWaveform(data):
                    # estrazione stringa dall'audio
                    recognized_data = extract_test_from()

        # riconoscimento offline fallito
        except ():
            return False, VERIFIED_A_PROBLEM_ITA \
                if self.language == Language.ITALIANO.value else \
                False, VERIFIED_A_PROBLEM_ENG

        # rimozione audio salvato
        os.remove(REC_AUDIO)

        # normalizzazione maiuscole e accenti
        recognized_data = normalize(recognized_data)

        # ritorno stringa del comando vocale
        print("Tu: " + recognized_data)
        return True, recognized_data
