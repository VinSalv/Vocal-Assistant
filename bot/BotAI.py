import asyncio
import logging
import os
import platform
from datetime import datetime

import python_weather
from chatterbot import ChatBot
from chatterbot.comparisons import levenshtein_distance
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ListTrainer

from utilities.Language import Language
from utilities.utils import greet_morning_in, greet_afternoon_in, greet_evening_in, \
    greet_night_in, actually_is_morning, actually_is_afternoon, actually_is_evening, actually_is_night, \
    know_name_bot_from, know_time_from, know_date_from, \
    know_weather_from, exit_from

logging.basicConfig(level=logging.CRITICAL)


# noinspection PyShadowingNames
class BotAI:
    bot = None
    name = ""
    voice_and_recognition = None
    language = ""
    cities = None

    def __init__(self, name, voice_and_recognition, cities):
        self.name = name
        self.bot = ChatBot(
            name,
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            database="./db.sqlite3",
            logic_adapters=[
                "chatterbot.logic.BestMatch"
            ],
            statement_comparison_function=levenshtein_distance,
            response_selection_method=get_random_response
        )
        self.voice_and_recognition = voice_and_recognition
        self.language = voice_and_recognition.speech_language
        self.cities = cities

    def train(self):
        # addestramento con esempio di comunicazione
        if self.language == Language.ITALIANO.value:
            with open("./example_of_communication/comunicazione_di_addestramento") as f:
                conversation = f.readlines()
                trainer = ListTrainer(self.bot)
                trainer.train(conversation)
        else:
            with open("./example_of_communication/training_communication") as f:
                conversation = f.readlines()
                trainer = ListTrainer(self.bot)
                trainer.train(conversation)

    def get_name_bot(self):
        if self.language == Language.ITALIANO.value:
            return f"Mi chiamo {self.name}, ma tu puoi chiamarmi come vuoi!"
        else:
            return f"My name is {self.name}, but you can call me whatever you want!"

    def get_date(self):
        def convert_number_to_word(month_number):
            if self.language == Language.ITALIANO.value:
                if month_number == "1" or month_number == "01":
                    return "Gennaio"
                elif month_number == "2" or month_number == "02":
                    return "Febbraio"
                elif month_number == "3" or month_number == "03":
                    return "Marzo"
                elif month_number == "4" or month_number == "04":
                    return "Aprile"
                elif month_number == "5" or month_number == "05":
                    return "Maggio"
                elif month_number == "6" or month_number == "06":
                    return "Giugno"
                elif month_number == "7" or month_number == "07":
                    return "Luglio"
                elif month_number == "8" or month_number == "08":
                    return "Agosto"
                elif month_number == "9" or month_number == "09":
                    return "Settembre"
                elif month_number == "10":
                    return "Ottobre"
                elif month_number == "11":
                    return "Novembre"
                elif month_number == "12":
                    return "Dicembre"
            else:
                if month_number == "1" or month_number == "01":
                    return "January"
                elif month_number == "2" or month_number == "02":
                    return "February"
                elif month_number == "3" or month_number == "03":
                    return "March"
                elif month_number == "4" or month_number == "04":
                    return "April"
                elif month_number == "5" or month_number == "05":
                    return "May"
                elif month_number == "6" or month_number == "06":
                    return "June"
                elif month_number == "7" or month_number == "07":
                    return "July"
                elif month_number == "8" or month_number == "08":
                    return "August"
                elif month_number == "9" or month_number == "09":
                    return "September"
                elif month_number == "10":
                    return "October"
                elif month_number == "11":
                    return "November"
                elif month_number == "12":
                    return "December"

            return month_word

        def translate_english_to_italian_(english_day_word):
            if english_day_word == "Monday":
                return "Lunedì"
            elif english_day_word == "Tuesday":
                return "Martedì"
            elif english_day_word == "Wednesday":
                return "Mercoledì"
            elif english_day_word == "Thursday":
                return "Giovedì"
            elif english_day_word == "Friday":
                return "Venerdì"
            elif english_day_word == "Saturday":
                return "Sabato"
            elif english_day_word == "Sunday":
                return "Domenica"

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
        if self.language == Language.ITALIANO.value:
            day_word = translate_english_to_italian_(day_word)

        # conversione del mese da numero a parola
        month_word = convert_number_to_word(month_number)

        # formula la data
        current_date = day_word + " " + day_number + " " + month_word + " " + year

        # ritorna la data
        if self.language == Language.ITALIANO.value:
            return f"Oggi è: {current_date}"
        else:
            return f"Today is: {current_date}"

    def get_time(self):
        # preleva l'orario e rimuovi gli zeri superflui
        if platform.system() == "Windows":
            current_time = datetime.now().strftime('%#H e %#M')
        else:
            current_time = datetime.now().strftime('%-H e %-M')

        # ritorna l'orario
        if self.language == Language.ITALIANO.value:
            return f"Sono le ore: {current_time}"
        else:
            return f"Are the hours: {current_time}"

    # noinspection GrazieInspection
    async def get_weather(self, recognized_data):

        # noinspection GrazieInspection
        def get_city_from(recognized_data):
            # dividi la frase in parole
            words = recognized_data.split()

            # verifica se esiste il nome di una città nel comando
            if len(words) > 2:

                # verifica se esiste il nome di una città con 4 parole
                if len(words) >= 4:
                    for index_word in range(len(words) - 3):
                        possible_city = words[index_word] + " " + \
                                        words[index_word + 1] + " " + \
                                        words[index_word + 2] + " " + \
                                        words[index_word + 3]
                        # verifica e ritorna la città
                        if possible_city in self.cities:
                            return True, possible_city

                # verifica se esiste il nome di una città con 3 parole
                if len(words) >= 3:
                    for index_word in range(len(words) - 2):
                        possible_city = words[index_word] + " " + \
                                        words[index_word + 1] + " " + \
                                        words[index_word + 2]
                        # verifica e ritorna la città
                        if possible_city in self.cities:
                            return True, possible_city

                # verifica se esiste il nome di una città con 2 parole
                if len(words) >= 2:
                    for index_word in range(len(words) - 1):
                        possible_city = words[index_word] + " " + \
                                        words[index_word + 1]
                        # verifica e ritorna la città
                        if possible_city in self.cities:
                            return True, possible_city

                # verifica se esiste il nome di una città con 1 parola
                for possible_city in words:
                    if possible_city in self.cities:
                        return True, possible_city

            # ritorna città non trovata
            if self.language == Language.ITALIANO.value:
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
                        if self.language == Language.ITALIANO.value:
                            forecast_three_days += f" --> ora: {hourly.time / 100} temperatura: " \
                                                   f"{hourly.temperature}C° {hourly.description} {hourly.type!r}\n"
                        else:
                            forecast_three_days += f" --> hour: {hourly.time / 100} temperature: " \
                                                   f"{hourly.temperature}C° {hourly.description} {hourly.type!r}\n"
                print(city + "\n" + forecast_three_days)

                # ritorna informazioni meteorologiche e astronomiche della città
                if self.language == Language.ITALIANO.value:
                    return "Attualmente a " + city + " ci sono " + current_temperature + \
                           " gradi centigradi. Ti mostro le previsioni nei prossimi 2 giorni e i dettagli astronomici."
                else:
                    return "Currently at " + city + " there are " + current_temperature + \
                           "degrees centigrade. I show you the forecast over the next 2 days and astronomical details."

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

    def get_correct_greeting_in(self):
        # ritorna la correzione da parte del bot
        if actually_is_morning:
            if self.language == Language.ITALIANO.value:
                return "Sono le " + str(datetime.now().hour) + " del mattino. Buon giorno!"
            else:
                return "It is " + str(datetime.now().hour) + " in the morning. Good morning!"
        elif actually_is_afternoon:
            if self.language == Language.ITALIANO.value:
                return "Sono le " + str(datetime.now().hour) + " del pomeriggio. Buon pomeriggio!"
            else:
                return "It is " + str(datetime.now().hour) + " in the afternoon. Good afternoon!"
        elif actually_is_evening:
            if self.language == Language.ITALIANO.value:
                return "Sono le " + str(datetime.now().hour) + " di sera. Buona sera!"
            else:
                return "It is " + str(datetime.now().hour) + " in the evening. Good evening!"
        else:
            if self.language == Language.ITALIANO.value:
                return "Sono le " + str(datetime.now().hour) + " di notte. Buona notte!"
            else:
                return "It is " + str(datetime.now().hour) + " at night. Good night!"

    def get_response(self, recognized_data):
        # esci
        if exit_from(recognized_data):
            return None

        # restituisci nome bot
        elif know_name_bot_from(recognized_data):
            return self.get_name_bot()

        # restituisci orario
        elif know_time_from(recognized_data):
            return self.get_time()

        # restituisci data
        elif know_date_from(recognized_data):
            return self.get_date()

        # restituisci meteo
        elif know_weather_from(recognized_data):
            if os.name == "nt":
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            return asyncio.run(self.get_weather(recognized_data))

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
                    response = self.get_correct_greeting_in()
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
            return response.encode(encoding="ascii", errors="ignore").decode()
