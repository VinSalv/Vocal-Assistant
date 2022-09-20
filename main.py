import platform
from datetime import datetime

import pyttsx3
import speech_recognition

from Jarvis import setup_jarvis
from VoiceAssistant import setup_assistant_voice, record_and_recognize_audio, \
    play_voice_assistant_speech, VoiceAssistant


def get_date(speech_language):
    # preleva data
    date_format = ""
    if platform.system() == "Windows":
        date_format = datetime.now().strftime("%#d/%#m/%Y")
    else:
        date_format = datetime.now().strftime("%-d/%-m/%Y")
    day_word = datetime.now().strftime('%A')

    # separa data
    splitted_date = date_format.split('/')
    day_number = splitted_date[0]
    month = splitted_date[1]
    year = splitted_date[2]

    # traduzione del giorno
    if speech_language == "it-IT":
        if day_word == "Monday":
            day_word = "Lunedì"
        elif day_word == "Tuesday":
            day_word = "Martedì"
        elif day_word == "Wednesday":
            day_word = "Mercoledì"
        elif day_word == "Thursday":
            day_word = "Giovedì"
        elif day_word == "Friday":
            day_word = "Venerdì"
        elif day_word == "Saturday":
            day_word = "Sabato"
        elif day_word == "Sunday":
            day_word = "Domenica"
    else:
        if day_word == "Lunedì":
            day_word = "Monday"
        elif day_word == "Martedì":
            day_word = "Tuesday"
        elif day_word == "Mercoledì":
            day_word = "Wednesday"
        elif day_word == "Giovedì":
            day_word = "Thursday"
        elif day_word == "Venerdì":
            day_word = "Friday"
        elif day_word == "Sabato":
            day_word = "Saturday"
        elif day_word == "Domenica":
            day_word = "Sunday"

    # traduzione del mese
    if speech_language == "it-IT":
        if month == "1":
            month = "Gennaio"
        elif month == "2":
            month = "Febbraio"
        elif month == "3":
            month = "Marzo"
        elif month == "4":
            month = "Aprile"
        elif month == "5":
            month = "Maggio"
        elif month == "6":
            month = "Giugno"
        elif month == "7":
            month = "Luglio"
        elif month == "8":
            month = "Agosto"
        elif month == "9":
            month = "Settembre"
        elif month == "10":
            month = "Ottobre"
        elif month == "11":
            month = "Novembre"
        elif month == "12":
            month = "Dicembre"
    else:
        if month == "1":
            month = "January"
        elif month == "2":
            month = "February"
        elif month == "3":
            month = "March"
        elif month == "4":
            month = "April"
        elif month == "5":
            month = "May"
        elif month == "6":
            month = "June"
        elif month == "7":
            month = "July"
        elif month == "8":
            month = "August"
        elif month == "9":
            month = "September"
        elif month == "10":
            month = "October"
        elif month == "11":
            month = "November"
        elif month == "12":
            month = "December"

    return day_word + " " + day_number + " " + month + " " + year


def get_time(speech_language):
    if platform.system() == "Windows":
        return datetime.now().strftime('%H e %#m')
    else:
        return datetime.now().strftime('%H e %-m')


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

    # addestramento assistente vocale
    jarvis = setup_jarvis()

    while True:
        try:
            # riconoscimento comando
            recognized_data = record_and_recognize_audio(voice_assistant, microphone, recognizer)
            print(recognized_data)

            # genera risposta
            bot_response = ""
            if any(word in recognized_data for word in
                   ["esci", "spegniti", "exit", "turn off", "switch off"]):
                exit(0)

            elif any(word in recognized_data for word in
                     ["ore", "ora", "orario", "hours", "hour", "whattime"]):
                current_time = get_time(voice_assistant.speech_language)
                if voice_assistant.speech_language == "it-IT":
                    bot_response = f"sono le ore: {current_time}"
                else:
                    bot_response = f"are the hours: {current_time}"

            elif any(word in recognized_data for word in
                     ["data", "giorno", "mese", "anno", "date", "day", "month", "year"]):
                current_date = get_date(voice_assistant.speech_language)
                if voice_assistant.speech_language == "it-IT":
                    bot_response = f"oggi è : {current_date}"
                else:
                    bot_response = f"today is: {current_date}"

            else:
                bot_response = jarvis.get_response(recognized_data)

            # output vocale
            print(bot_response)
            play_voice_assistant_speech(tts_engine, bot_response)

        except(KeyboardInterrupt, EOFError, SystemExit):
            print("uscita!")
            exit(1)
