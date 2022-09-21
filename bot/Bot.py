import logging
import platform
from datetime import datetime

from chatterbot import ChatBot
from chatterbot.comparisons import levenshtein_distance
from chatterbot.response_selection import get_first_response
from chatterbot.trainers import ListTrainer

logging.basicConfig(level=logging.CRITICAL)


def get_date(language):
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
    if language == "it-IT":
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
    if language == "it-IT":
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


def get_time():
    if platform.system() == "Windows":
        return datetime.now().strftime('%#H e %#M')
    else:
        return datetime.now().strftime('%-H e %-M')


class Bot:
    bot = None
    name = ""

    def __init__(self, name):
        self.name = name
        self.bot = ChatBot(
            name,
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            database="./db.sqlite3",
            logic_adapters=[
                "chatterbot.logic.BestMatch"
            ],
            statement_comparison_function=levenshtein_distance,
            response_selection_method=get_first_response
        )

    def train(self, language):
        # addestramento con esempio di comunicazione
        if language == "it-IT":
            with open("./example_of_communication/comunicazione_di_addestramento") as f:
                conversation = f.readlines()
                trainer = ListTrainer(self.bot)
                trainer.train(conversation)
        else:
            with open("./example_of_communication/training_communication") as f:
                conversation = f.readlines()
                trainer = ListTrainer(self.bot)
                trainer.train(conversation)

    def get_response(self, recognized_data, language):
        # esci
        if any(word in recognized_data for word in
               ["esci", "spegniti", "exit", "turn off", "switch off"]):
            return None

        # restituisci nome bot
        elif recognized_data.__contains__("tuo nome") or \
                (recognized_data.__contains__("come") and recognized_data.__contains__("chiami")) or \
                recognized_data.__contains__("chiamarti") or \
                recognized_data.__contains__("your name") or \
                recognized_data.__contains__("call you"):
            if language == "it-IT":
                return f"mi chiamo {self.name}, ma tu puoi chiamarmi come vuoi!"
            else:
                return f"my name is {self.name}, but you can call me whatever you want!"

        # restituisci orario
        elif any(word in recognized_data for word in
                 ["ore", "ora", "orario", "hours", "hour", "whattime"]):
            current_time = get_time()
            if language == "it-IT":
                return f"sono le ore: {current_time}"
            else:
                return f"are the hours: {current_time}"

        # restituisci data
        elif any(word in recognized_data for word in
                 ["data", "giorno", "mese", "anno", "date", "day", "month", "year"]):
            current_date = get_date(language)
            if language == "it-IT":
                return f"oggi è: {current_date}"
            else:
                return f"today is: {current_date}"

        # restituisci risposta dato l'addestramento
        else:
            return self.bot.get_response(recognized_data.replace(self.name.lower(), ''))
