import asyncio
import logging
import os
import platform
from datetime import datetime

import python_weather
from chatterbot import ChatBot
from chatterbot.comparisons import synset_distance, levenshtein_distance, sentiment_comparison
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ListTrainer

from utilities.Language import Language
from utilities.util import extract_cities_from, greet_morning_in, greet_afternoon_in, greet_evening_in, \
    greet_night_in, actually_is_morning, actually_is_afternoon, actually_is_evening, actually_is_night, \
    know_name_bot_from, know_time_from, know_date_from, \
    know_weather_from, exit_from

logging.basicConfig(level=logging.CRITICAL)

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

    def get_name_bot(self, language):
        if language == Language.ITALIANO.value:
            return f"Mi chiamo {self.name}, ma tu puoi chiamarmi come vuoi!"
        else:
            return f"My name is {self.name}, but you can call me whatever you want!"

    @staticmethod
    def get_date(language):
        def convert_number_to_word(language, month_number):
            month_word = ""
            if language == Language.ITALIANO.value:
                if month_number == "1" or month_number == "01":
                    month_word = "Gennaio"
                elif month_number == "2" or month_number == "02":
                    month_word = "Febbraio"
                elif month_number == "3" or month_number == "03":
                    month_word = "Marzo"
                elif month_number == "4" or month_number == "04":
                    month_word = "Aprile"
                elif month_number == "5" or month_number == "05":
                    month_word = "Maggio"
                elif month_number == "6" or month_number == "06":
                    month_word = "Giugno"
                elif month_number == "7" or month_number == "07":
                    month_word = "Luglio"
                elif month_number == "8" or month_number == "08":
                    month_word = "Agosto"
                elif month_number == "9" or month_number == "09":
                    month_word = "Settembre"
                elif month_number == "10":
                    month_word = "Ottobre"
                elif month_number == "11":
                    month_word = "Novembre"
                elif month_number == "12":
                    month_word = "Dicembre"
            else:
                if month_number == "1" or month_number == "01":
                    month_word = "January"
                elif month_number == "2" or month_number == "02":
                    month_word = "February"
                elif month_number == "3" or month_number == "03":
                    month_word = "March"
                elif month_number == "4" or month_number == "04":
                    month_word = "April"
                elif month_number == "5" or month_number == "05":
                    month_word = "May"
                elif month_number == "6" or month_number == "06":
                    month_word = "June"
                elif month_number == "7" or month_number == "07":
                    month_word = "July"
                elif month_number == "8" or month_number == "08":
                    month_word = "August"
                elif month_number == "9" or month_number == "09":
                    month_word = "September"
                elif month_number == "10":
                    month_word = "October"
                elif month_number == "11":
                    month_word = "November"
                elif month_number == "12":
                    month_word = "December"

            return month_word

        def translate_english_to_italian_(english_day_word):
            italian_day_word = ""
            if english_day_word == "Monday":
                italian_day_word = "Lunedì"
            elif english_day_word == "Tuesday":
                italian_day_word = "Martedì"
            elif english_day_word == "Wednesday":
                italian_day_word = "Mercoledì"
            elif english_day_word == "Thursday":
                italian_day_word = "Giovedì"
            elif english_day_word == "Friday":
                italian_day_word = "Venerdì"
            elif english_day_word == "Saturday":
                italian_day_word = "Sabato"
            elif english_day_word == "Sunday":
                italian_day_word = "Domenica"
            return italian_day_word

        # preleva data e rimuovi gli zeri superflui
        if platform.system() == "Windows":
            date_format = datetime.now().strftime("%#d/%#m/%Y")
        else:
            date_format = datetime.now().strftime("%-d/%-m/%Y")
        day_word = datetime.now().strftime('%A')

        # separa campi della data
        splitted_date = date_format.split('/')
        day_number = splitted_date[0]
        month_number = splitted_date[1]
        year = splitted_date[2]

        # traduzione del giorno in italiano
        if language == Language.ITALIANO.value:
            day_word = translate_english_to_italian_(day_word)

        # conversione del mese da numero a parola
        month_word = convert_number_to_word(language, month_number)

        # formula la data
        current_date = day_word + " " + day_number + " " + month_word + " " + year

        # ritorna la data
        if language == Language.ITALIANO.value:
            return f"Oggi è: {current_date}"
        else:
            return f"Today is: {current_date}"

    @staticmethod
    def get_time(language):
        # preleva l'orario e rimuovi gli zeri superflui
        if platform.system() == "Windows":
            current_time = datetime.now().strftime('%#H e %#M')
        else:
            current_time = datetime.now().strftime('%-H e %-M')

        # ritorna l'orario
        if language == Language.ITALIANO.value:
            return f"Sono le ore: {current_time}"
        else:
            return f"Are the hours: {current_time}"

    @staticmethod
    async def get_weather(recognized_data, language):

        def get_city_from(recognized_data):
            # dividi la frase in parole
            words = recognized_data.split()

            # verifica se esiste il nome di una città nel comando
            if len(words) > 2:
                # preleva la lista delle città da un file in formato csv
                cities = extract_cities_from("./utilities/cities.csv")

                # verifica se esiste il nome di una città con 4 parole
                if len(words) >= 4:
                    for index_word in range(len(words) - 3):
                        possible_city = words[index_word] + " " + \
                                        words[index_word + 1] + " " + \
                                        words[index_word + 2] + " " + \
                                        words[index_word + 3]
                        # verifica e ritorna la città
                        if possible_city in cities:
                            return True, possible_city

                # verifica se esiste il nome di una città con 3 parole
                if len(words) >= 3:
                    for index_word in range(len(words) - 2):
                        possible_city = words[index_word] + " " + \
                                        words[index_word + 1] + " " + \
                                        words[index_word + 2]
                        # verifica e ritorna la città
                        if possible_city in cities:
                            return True, possible_city

                # verifica se esiste il nome di una città con 2 parole
                if len(words) >= 2:
                    for index_word in range(len(words) - 1):
                        possible_city = words[index_word] + " " + \
                                        words[index_word + 1]
                        # verifica e ritorna la città
                        if possible_city in cities:
                            return True, possible_city

                # verifica se esiste il nome di una città con 1 parola
                for possible_city in words:
                    if possible_city in cities:
                        return True, possible_city

            # ritorna città non trovata
            if language == Language.ITALIANO.value:
                return False, "Mi spiace. Non ho capito il nome della città."
            else:
                return False, "I'm sorry. I didn't get the name of the city."

        async with python_weather.Client(format=python_weather.METRIC) as client:
            # verifica se esiste una città
            city_is_found, response = get_city_from(recognized_data)

            # rilevata la città
            if city_is_found:

                # preleva informazioni meteorologiche e astronomiche della città
                city = response
                weather = await client.get(city)

                # preleva temperatura attuale
                current_temperature = str(weather.current.temperature)

                # previsione di 3 giorni consecutivi
                forecast_three_days = ""
                for forecast in weather.forecasts:
                    forecast_three_days += str(forecast.date) + "\n"
                    forecast_three_days += str(forecast.astronomy) + "\n"
                    for hourly in forecast.hourly:
                        if language == Language.ITALIANO.value:
                            forecast_three_days += f" --> ora: {hourly.time / 100} temperatura: {(hourly.temperature)}C° {hourly.description} {hourly.type!r}\n"
                        else:
                            forecast_three_days += f" --> hour: {hourly.time / 100} temperature: {(hourly.temperature)}C° {hourly.description} {hourly.type!r}\n"
                print(city + "\n" + forecast_three_days)

                # ritorna informazioni meteorologiche e astronomiche della città
                if language == Language.ITALIANO.value:
                    return "Attualmente a " + city + " ci sono " + current_temperature + " gradi centigradi. Ti mostro le previsioni nei prossimi 2 giorni e i dettagli astronomici."
                else:
                    return "Currently at " + city + " there are " + current_temperature + "degrees centigrade. I show you the forecast over the next 2 days and astronomical details."

            # città non rilevata
            else:
                return response

    @staticmethod
    def what_is_in(recognized_data):
        # il comando potrebbe contenere un saluto specifico, un semplice saluto o altro
        is_greeting = False
        correct_greeting = False

        # verifica se il comando contiene lo specifico saluto del buon giorno
        if greet_morning_in(recognized_data):
            # verifica se il saluto è corretto
            if actually_is_morning:
                is_greeting = True
                correct_greeting = True
            else:
                is_greeting = True
                correct_greeting = False

        # verifica se il comando contiene lo specifico saluto del buon pomeriggio
        elif greet_afternoon_in(recognized_data):
            # verifica se il saluto è corretto
            if actually_is_afternoon:
                is_greeting = True
                correct_greeting = True
            else:
                is_greeting = True
                correct_greeting = False

        # verifica se il comando contiene lo specifico saluto della buon sera
        elif greet_evening_in(recognized_data):
            # verifica se il saluto è corretto
            if actually_is_evening:
                is_greeting = True
                correct_greeting = True
            else:
                is_greeting = True
                correct_greeting = False

        # verifica se il comando contiene lo specifico saluto della buona notte
        elif greet_night_in(recognized_data):
            # verifica se il saluto è corretto
            if actually_is_night:
                is_greeting = True
                correct_greeting = True
            else:
                is_greeting = True
                correct_greeting = False

        # ritorna cosa è stato rilevato
        return is_greeting, correct_greeting

    @staticmethod
    def get_correct_greeting_in(language):
        # ritorna la correzione da parte del bot
        if actually_is_morning:
            if language == Language.ITALIANO.value:
                return "Sono le " + str(datetime.now().hour) + " del mattino. Buon giorno!"
            else:
                return "It is " + str(datetime.now().hour) + " in the morning. Good morning!"
        elif actually_is_afternoon:
            if language == Language.ITALIANO.value:
                return "Sono le " + str(datetime.now().hour) + " del pomeriggio. Buon pomeriggio!"
            else:
                return "It is " + str(datetime.now().hour) + " in the afternoon. Good afternoon!"
        elif actually_is_evening:
            if language == Language.ITALIANO.value:
                return "Sono le " + str(datetime.now().hour) + " di sera. Buona sera!"
            else:
                return "It is " + str(datetime.now().hour) + " in the evening. Good evening!"
        else:
            if language == Language.ITALIANO.value:
                return "Sono le " + str(datetime.now().hour) + " di notte. Buona notte!"
            else:
                return "It is " + str(datetime.now().hour) + " at night. Good night!"

    def get_response(self, recognized_data, language):
        # esci
        if exit_from(recognized_data):
            return None

        # restituisci nome bot
        elif know_name_bot_from(recognized_data):
            return self.get_name_bot(language)

        # restituisci orario
        elif know_time_from(recognized_data):
            return self.get_time(language)

        # restituisci data
        elif know_date_from(recognized_data):
            return self.get_date(language)

        # restituisci meteo
        elif know_weather_from(recognized_data):
            if os.name == "nt":
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            return asyncio.run(self.get_weather(recognized_data, language))

        # restituisci risposta data dall'addestramento e verifica un eventuale saluto
        else:
            # formula una risposta del bot
            response = str(self.bot.get_response(recognized_data.replace(self.name.lower(), '')))

            # verifica l'eventuale saluto o altro da parte dell'interlocutore
            is_greeting, correct_greeting = self.what_is_in(recognized_data)

            # saluto dell'interlocutore
            if is_greeting:
                # saluto non appropriato
                if not correct_greeting:
                    response = self.get_correct_greeting_in(language)
            else:

                # verifica l'eventuale saluto da parte del bot
                while True:
                    is_greeting, correct_greeting = self.what_is_in(response)
                    # saluto del bot, ma non appropriato
                    if is_greeting and not correct_greeting:
                        response = str(self.bot.get_response(recognized_data.replace(self.name.lower(), '')))
                    # saluto semplice o altro
                    else:
                        break

            # ritorna la risposta
            return response
