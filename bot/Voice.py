import pyttsx3

from utilities.Language import Language


class Voice:
    name_bot = ""
    language = ""
    name_voice = ""
    sex_voice = ""
    tts_engine = pyttsx3.init()

    def __init__(self, name_bot, language, name_voice, sex_voice):
        self.name_bot = name_bot
        self.language = language
        self.name_voice = name_voice
        self.sex = sex_voice
        self.setup_bot_voice()

    def setup_bot_voice(self):
        # settaggio lingua del bot
        voices = self.tts_engine.getProperty("voices")
        self.tts_engine.setProperty("voice", voices[2].id) \
            if self.language == Language.ITALIANO.value \
            else self.tts_engine.setProperty("voice", voices[0].id)

        # velocità del parlato del bot
        self.tts_engine.setProperty("rate", 150)

    def output_response_bot(self, bot_response):
        # stampa e comunicazione della risposta
        print(self.name_bot + ": " + str(bot_response))
        self.play_voice_bot(bot_response)

    def play_voice_bot(self, bot_response):
        self.tts_engine.say(str(bot_response))
        self.tts_engine.runAndWait()
        self.tts_engine.stop()
