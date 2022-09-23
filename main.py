import os

import speech_recognition
from vosk import Model

from bot.BotAI import BotAI
from bot.VoiceAndRecognition import VoiceAndRecognition
from utilities.Language import Language
from utilities.utils import extract_cities_from

name_bot = "Jarvis"
language = Language.ITALIANO.value
cities = extract_cities_from("./utilities/cities.csv")


def init_recognizer_offline():
    # estrai modello di riconoscimento offline
    if language == Language.ITALIANO.value:
        if not os.path.exists("./models/modello_italiano"):
            print("Scaricare il modello da:\n"
                  "https://alphacephei.com/vosk/models e decomprimere nella cartella models.")
            exit(1)
        return Model("./models/modello_italiano")
    else:
        if not os.path.exists("./models/modello_inglese"):
            print("Scaricare il modello da:\n"
                  "https://alphacephei.com/vosk/models e decomprimere nella cartella models.")
            exit(1)
        return Model("./models/modello_inglese")


def init_recognizer_online():
    # estrai modello di riconoscimento online
    return speech_recognition.Recognizer()


def init_recognizers():
    return init_recognizer_online(), init_recognizer_offline()


if __name__ == '__main__':

    # inizializzazione del microfono
    microphone = speech_recognition.Microphone()

    # inizializzazione del riconoscimento vocale
    recognizer_online, recognizer_offline = init_recognizers()

    # istanza del bot
    if not os.path.exists("./db.sqlite3"):
        bot = BotAI(name=name_bot,
                    voice_and_recognition=VoiceAndRecognition(name="",
                                                              sex="",
                                                              speech_language=language,
                                                              recognition_language=language),
                    cities=cities)
        # addestramento del bot
        bot.train()
    else:
        bot = BotAI(name=name_bot,
                    voice_and_recognition=VoiceAndRecognition(name="",
                                                              sex="",
                                                              speech_language=language,
                                                              recognition_language=language),
                    cities=cities)

    while True:
        try:
            # riconoscimento comando
            recognized_data = bot.voice_and_recognition.use_recognition_online(microphone,
                                                                               recognizer_online,
                                                                               recognizer_offline)
            if len(recognized_data) > 0:
                # genera risposta
                bot_response = bot.get_response(recognized_data)

                # nessuna risposta quindi exit
                if bot_response is None:
                    bot.voice_and_recognition.output_response(name_bot, "Va bene. A presto!")
                    break

                # manda la risposta in output
                bot.voice_and_recognition.output_response(name_bot, bot_response)

        except(KeyboardInterrupt, EOFError, SystemExit):
            bot.voice_and_recognition.output_response("Si è verificato un problema! Riprova più tardi.")
            exit(1)

    exit(0)
