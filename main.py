import pyttsx3
import speech_recognition

from utilities.Language import Language
from bot.Bot import Bot
from bot.VoiceAndRecognition import VoiceAndRecognition

if __name__ == '__main__':
    # inizializzazione del riconoscimento vocale e del microfono
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # inizializzazione voce e comprensione del bot
    language = Language.ITALIANO
    voice_and_recognition = VoiceAndRecognition(name="",
                                                sex="",
                                                speech_language=language,
                                                recognition_language=language)

    # inizializzazione dello strumento di sintesi vocale
    tts_engine = pyttsx3.init()
    tts_engine = voice_and_recognition.setup_bot_voice(tts_engine)

    # istanza e addestramento del bot
    name_bot = "Jarvis"
    bot = Bot(name=name_bot)
    bot.train(voice_and_recognition.speech_language)

    while True:
        try:
            # riconoscimento comando
            recognized_data = voice_and_recognition.record_and_recognize_audio(microphone, recognizer)

            if len(recognized_data) > 0:
                print("Tu: " + recognized_data)

                # genera risposta
                bot_response = bot.get_response(recognized_data, language)
                if bot_response is None:
                    break

                # output vocale
                print(name_bot + ": " + str(bot_response))
                voice_and_recognition.play_voice_bot_speech(tts_engine, bot_response)

        except(KeyboardInterrupt, EOFError, SystemExit):
            print("uscita!")
            exit(1)

    exit(0)
