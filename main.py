import os

from bot.BotAI import BotAI
from bot.Recognition import Recognition
from bot.Voice import Voice
from utilities.Language import Language
from utilities.utils import VERIFIED_A_PROBLEM_ITA, VERIFIED_A_PROBLEM_ENG, EXIT_ITA, EXIT_ENG, KNOWLEDGE, ready_text

name_bot = "Jarvis"
language = Language.ITALIANO.value

if __name__ == '__main__':
    # istanza del bot
    if not os.path.exists(KNOWLEDGE):
        bot = BotAI(name_bot=name_bot,
                    language=language,
                    recognition=Recognition(name_bot=name_bot, language=language),
                    voice=Voice(name_bot=name_bot, language=language, name_voice="", sex_voice=""))
        # addestramento del bot
        bot.train()
    else:
        bot = BotAI(name_bot=name_bot,
                    language=language,
                    recognition=Recognition(name_bot=name_bot, language=language),
                    voice=Voice(name_bot=name_bot, language=language, name_voice="", sex_voice=""))

    # bot in funzione
    bot.voice.output_response_bot(ready_text)
    while True:
        try:
            # riconoscimento comando
            data_is_recognized, returned_text = bot.recognition.use_recognition_online()

            # riconoscimento comando vocale avvenuto con successo
            if data_is_recognized:
                recognized_data = returned_text

                # genera risposta
                bot_response = bot.get_response(recognized_data)

                # nessuna risposta quindi exit
                if bot_response is None:
                    bot.voice.output_response_bot(EXIT_ITA if language == Language.ITALIANO.value else EXIT_ENG)
                    break

                # manda la risposta in output
                bot.voice.output_response_bot(bot_response)

            # problemi riconoscimento comando vocale
            else:
                if returned_text is not None:
                    bot.voice.output_response_bot(returned_text)

        # crash del programma
        except():
            bot.voice.output_response_bot(VERIFIED_A_PROBLEM_ITA
                                          if language == Language.ITALIANO.value
                                          else VERIFIED_A_PROBLEM_ENG)
            exit(1)

    exit(0)
