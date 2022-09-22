import asyncio
import logging
import os
import platform
from datetime import datetime

import python_weather
from chatterbot import ChatBot
from chatterbot.comparisons import sentiment_comparison
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ListTrainer

from utilities.Language import Language
from utilities.util import extract_cities_from, greet_morning_in, greet_afternoon_in, greet_evening_in, \
    greet_night_in, MORNING, AFTERNOON, EVENING, NIGHT

logging.basicConfig(level=logging.CRITICAL)


def get_date(language):
    # preleva data
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
    if language == Language.ITALIANO.value:
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
    if language == Language.ITALIANO.value:
        if month == "1" or month == "01":
            month = "Gennaio"
        elif month == "2" or month == "02":
            month = "Febbraio"
        elif month == "3" or month == "03":
            month = "Marzo"
        elif month == "4" or month == "04":
            month = "Aprile"
        elif month == "5" or month == "05":
            month = "Maggio"
        elif month == "6" or month == "06":
            month = "Giugno"
        elif month == "7" or month == "07":
            month = "Luglio"
        elif month == "8" or month == "08":
            month = "Agosto"
        elif month == "9" or month == "09":
            month = "Settembre"
        elif month == "10":
            month = "Ottobre"
        elif month == "11":
            month = "Novembre"
        elif month == "12":
            month = "Dicembre"
    else:
        if month == "1" or month == "01":
            month = "January"
        elif month == "2" or month == "02":
            month = "February"
        elif month == "3" or month == "03":
            month = "March"
        elif month == "4" or month == "04":
            month = "April"
        elif month == "5" or month == "05":
            month = "May"
        elif month == "6" or month == "06":
            month = "June"
        elif month == "7" or month == "07":
            month = "July"
        elif month == "8" or month == "08":
            month = "August"
        elif month == "9" or month == "09":
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


def fahrenheit_to_celsius(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9)


async def getweather(city, language):
    # declare the client. format defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(format=python_weather.IMPERIAL) as client:
        # fetch a weather forecast from a city
        weather = await client.get(city)

        # returns the current day's forecast temperature (int)
        celsius = str(fahrenheit_to_celsius(weather.current.temperature))
        print("attualmente a " + city + " ci sono " + celsius + "C°")

        # get the weather forecast for a few days
        for forecast in weather.forecasts:
            print(forecast.date, forecast.astronomy)

            # hourly forecasts
            for hourly in forecast.hourly:
                print(
                    f' --> {hourly.time / 100} {fahrenheit_to_celsius(hourly.temperature)}C° {hourly.description} {hourly.type!r}')

        if language == Language.ITALIANO.value:
            return "attualmente a " + city + " ci sono " + celsius + " gradi centigradi. In seguito puoi vedere le previsioni nei prossimi 2 giorni e dettagli astronomici."
        else:
            return "currently at " + city + " there are " + celsius + "degrees centigrade. Next you can see the forecast over the next 2 days and astronomical details."


def right_greeting_in(string):
    if greet_morning_in(string):
        if not MORNING:
            return False
    elif greet_afternoon_in(string):
        if not AFTERNOON:
            return False
    elif greet_evening_in(string):
        if not EVENING:
            return False
    elif greet_night_in(string):
        if not NIGHT:
            return False
    # potrebbe anche non essere un saluto
    return True


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
            statement_comparison_function=sentiment_comparison,
            response_selection_method=get_random_response
        )

    def train(self, language):
        # addestramento con esempio di comunicazione
        if language == Language.ITALIANO.value:
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
        if any(word in recognized_data.split(" ") for word in
               ["esci", "spegniti", "exit", "turn off", "switch off"]):
            return None

        # restituisci nome bot
        elif recognized_data.__contains__("tuo nome") or \
                (recognized_data.__contains__("come") and recognized_data.__contains__("chiami")) or \
                (recognized_data.__contains__("che") and recognized_data.__contains__("nome")) or \
                recognized_data.__contains__("chiamarti") or \
                recognized_data.__contains__("your name") or \
                (recognized_data.__contains__("what") and recognized_data.__contains__("name")) or \
                recognized_data.__contains__("call you"):
            if language == Language.ITALIANO.value:
                return f"mi chiamo {self.name}, ma tu puoi chiamarmi come vuoi!"
            else:
                return f"my name is {self.name}, but you can call me whatever you want!"

        # restituisci orario
        elif any(word in recognized_data.replace("'", " ").split(" ") for word in
                 ["ore", "ora", "orario", "hours", "hour"]) \
                or recognized_data.__contains__("what time"):
            current_time = get_time()
            if language == Language.ITALIANO.value:
                return f"sono le ore: {current_time}"
            else:
                return f"are the hours: {current_time}"

        # restituisci data
        elif any(word in recognized_data.split(" ") for word in
                 ["data", "mese", "anno", "date", "day", "month", "year"]) or \
                recognized_data.__contains__("quale") and recognized_data.__contains__("giorno") or \
                recognized_data.__contains__("che") and recognized_data.__contains__("giorno") or \
                recognized_data.__contains__("giorno") and recognized_data.__contains__("di"):
            current_date = get_date(language)
            if language == Language.ITALIANO.value:
                return f"oggi è: {current_date}"
            else:
                return f"today is: {current_date}"

        # restituisci meteo
        elif any(word in recognized_data.split(" ") for word in
                 ["meteo", "weather", "forecast"]) or \
                recognized_data.__contains__("previsioni del tempo") or \
                recognized_data.__contains__("come è il tempo") or \
                recognized_data.__contains__("com è il tempo") or \
                recognized_data.__contains__("com'è il tempo") or \
                recognized_data.__contains__("quale è il tempo") or \
                recognized_data.__contains__("qual è il tempo") or \
                recognized_data.__contains__("qual' è il tempo") or \
                recognized_data.__contains__("che tempo") or \
                recognized_data.__contains__("il tempo a"):

            if os.name == "nt":
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

            words = recognized_data.split()

            cities = []
            if len(words) > 2:
                cities = extract_cities_from("./utilities/cities.csv")

            if len(words) >= 4:
                for index_word in range(len(words) - 3):
                    possible_city = words[index_word] + " " + \
                                    words[index_word + 1] + " " + \
                                    words[index_word + 2] + " " + \
                                    words[index_word + 3]
                    if possible_city in cities:
                        response = asyncio.run(getweather(possible_city, language))
                        return response

            if len(words) >= 3:
                for index_word in range(len(words) - 2):
                    possible_city = words[index_word] + " " + \
                                    words[index_word + 1] + " " + \
                                    words[index_word + 2]
                    if possible_city in cities:
                        response = asyncio.run(getweather(possible_city, language))
                        return response

            if len(words) >= 2:
                for index_word in range(len(words) - 1):
                    possible_city = words[index_word] + " " + \
                                    words[index_word + 1]
                    if possible_city in cities:
                        response = asyncio.run(getweather(possible_city, language))
                        return response

            for possible_city in words:
                if possible_city in cities:
                    response = asyncio.run(getweather(possible_city, language))
                    return response

            if language == Language.ITALIANO.value:
                return "mi spiace. Non ho capito il nome della città."
            else:
                return "I'm sorry. I didn't get the name of the city."

        # restituisci risposta dato l'addestramento e verifica il saluto
        else:
            response = str(self.bot.get_response(recognized_data.replace(self.name.lower(), '')))
            # verifica l'eventuale saluto da parte dell'interlocutore
            if not right_greeting_in(recognized_data):
                if MORNING:
                    if language == Language.ITALIANO.value:
                        response = "sono le " + str(datetime.now().hour) + " del mattino. buon giorno!"
                    else:
                        response = "it is " + str(datetime.now().hour) + " in the morning. good morning!"
                elif AFTERNOON:
                    if language == Language.ITALIANO.value:
                        response = "sono le " + str(datetime.now().hour) + " del pomeriggio. buon pomeriggio!"
                    else:
                        response = "it is " + str(datetime.now().hour) + " in the afternoon. good afternoon!"
                elif EVENING:
                    if language == Language.ITALIANO.value:
                        response = "sono le " + str(datetime.now().hour) + " di sera. buona sera!"
                    else:
                        response = "it is " + str(datetime.now().hour) + " in the evening. good evening!"
                elif NIGHT:
                    if language == Language.ITALIANO.value:
                        response = "sono le " + str(datetime.now().hour) + " di notte. buona notte!"
                    else:
                        response = "it is " + str(datetime.now().hour) + " at night. good night!"
            else:
                # verifica l'eventuale saluto da parte del bot
                while True:
                    if not right_greeting_in(response):
                        response = str(self.bot.get_response(recognized_data.replace(self.name.lower(), '')))
                    else:
                        break

            return response
