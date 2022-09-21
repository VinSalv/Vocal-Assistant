import pyttsx3
import speech_recognition

from assistantSpeachAndRecognition.VoiceAssistant import setup_assistant_voice, record_and_recognize_audio, \
    play_voice_assistant_speech, VoiceAssistant
from bot.Bot import Bot

if __name__ == '__main__':

    # inizializzazione del riconoscimento vocale e del microfono
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # inizializzazione dello strumento di sintesi vocale
    tts_engine = pyttsx3.init()

    # impostazione dei dati dell'assistente vocale
    voice_assistant = VoiceAssistant(name="Mark", sex="male", speech_language="it-IT", recognition_language="it-IT")

    # impostazione della voce dell'assistente vocale
    tts_engine = setup_assistant_voice(tts_engine, voice_assistant)

    # istanza e addestramento del bot
    name_bot = "Jarvis"
    bot = Bot(name=name_bot)
    bot.train(voice_assistant.speech_language)

    while True:
        try:
            # riconoscimento comando
            recognized_data = record_and_recognize_audio(voice_assistant, microphone, recognizer)
            print(recognized_data)

            if len(recognized_data) > 0:
                # genera risposta
                bot_response = bot.get_response(recognized_data, voice_assistant)
                if bot_response is None:
                    break

                # output vocale
                print(bot_response)
                play_voice_assistant_speech(tts_engine, bot_response)

        except(KeyboardInterrupt, EOFError, SystemExit):
            print("uscita!")
            exit(1)

    exit(0)
