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
    know_weather_from, exit_from, MAX_OVERCAST_ITA, MAX_OVERCAST_ENG, MORE_OVERCAST_ITA, MORE_OVERCAST_ENG, \
    ENOUGH_OVERCAST_ITA, ENOUGH_OVERCAST_ENG, MIN_OVERCAST_ITA, MIN_OVERCAST_ENG, NOTHING_OVERCAST_ITA, \
    NOTHING_OVERCAST_ENG, MAX_THUNDER_ITA, MAX_THUNDER_ENG, MORE_THUNDER_ITA, MORE_THUNDER_ENG, ENOUGH_THUNDER_ITA, \
    ENOUGH_THUNDER_ENG, MIN_THUNDER_ITA, MIN_THUNDER_ENG, NOTHING_THUNDER_ITA, NOTHING_THUNDER_ENG, MAX_RAIN_ITA, \
    MAX_RAIN_ENG, MORE_RAIN_ITA, MORE_RAIN_ENG, ENOUGH_RAIN_ITA, ENOUGH_RAIN_ENG, MIN_RAIN_ITA, MIN_RAIN_ENG, \
    NOTHING_RAIN_ITA, NOTHING_RAIN_ENG, MAX_SNOW_ITA, MAX_SNOW_ENG, MORE_SNOW_ITA, MORE_SNOW_ENG, ENOUGH_SNOW_ITA, \
    ENOUGH_SNOW_ENG, MIN_SNOW_ITA, MIN_SNOW_ENG, NOTHING_SNOW_ITA, NOTHING_SNOW_ENG, MORE_HIGHTEMP_ITA, \
    MORE_HIGHTEMP_ENG, MIN_HIGHTEMP_ITA, MIN_HIGHTEMP_ENG, MORE_FOREST_ITA, MORE_FOREST_ENG, MIN_FOREST_ITA, \
    MIN_FOREST_ENG, MAX_WINDY_ITA, MAX_WINDY_ENG, MORE_WINDY_ITA, MORE_WINDY_ENG, ENOUGH_WINDY_ITA, ENOUGH_WINDY_ENG, \
    MIN_WINDY_ITA, MIN_WINDY_ENG, NOTHING_WINDY_ITA, NOTHING_WINDY_ENG, MAX_HUMIDITY_ITA, MAX_HUMIDITY_ENG, \
    MORE_HUMIDITY_ITA, MORE_HUMIDITY_ENG, ENOUGH_HUMIDITY_ITA, ENOUGH_HUMIDITY_ENG, MIN_HUMIDITY_ITA, \
    MIN_HUMIDITY_ENG, NOTHING_HUMIDITY_ITA, NOTHING_HUMIDITY_ENG, MAX_FOG_ITA, MAX_FOG_ENG, MORE_FOG_ITA, \
    MORE_FOG_ENG, ENOUGH_FOG_ITA, ENOUGH_FOG_ENG, MIN_FOG_ITA, MIN_FOG_ENG, NOTHING_FOG_ITA, NOTHING_FOG_ENG, \
    CORRECT_AFTERNOON_ITA, CORRECT_AFTERNOON_ENG, CORRECT_EVENING_ITA, CORRECT_EVENING_ENG, CORRECT_NIGHT_ITA, \
    CORRECT_MORNING_ITA, CORRECT_MORNING_ENG, CORRECT_NIGHT_ENG, TIME_ITA, TIME_ENG

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
        return f"Mi chiamo {self.name}, ma tu puoi chiamarmi come vuoi!" \
            if self.language == Language.ITALIANO.value else \
            f"My name is {self.name}, but you can call me whatever you want!"

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
        date_format = datetime.now().strftime("%#d/%#m/%Y") \
            if platform.system() == "Windows" else \
            datetime.now().strftime("%-d/%-m/%Y")
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
        return f"Oggi è: {current_date}" if self.language == Language.ITALIANO.value else f"Today is: {current_date}"

    def get_time(self):
        # ritorna l'orario
        return TIME_ITA if self.language == Language.ITALIANO.value else TIME_ENG

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

        # noinspection GrazieInspection
        def get_other_info(city, weather):
            # previsione di 3 giorni consecutivi
            forecast_three_days = ""

            # percentuale fenomeni meteorologici
            is_current_forecast = True
            remaining_hours_within_current_day = 0
            chance_of_fog = 0
            chance_of_frost = 0
            chance_of_windy = 0
            chance_of_rain = 0
            chance_of_snow = 0
            chance_of_hightemp = 0
            chance_of_overcast = 0
            chance_of_humidity = 0
            chance_of_thunder = 0

            # preleva informazioni meteorologiche e astronomiche
            for forecast in weather.forecasts:
                # preleva data a cui fa riferimento la seguente previsione
                forecast_three_days += str(forecast.date) + "\n"
                # preleva informazioni astronomiche
                forecast_three_days += str(forecast.astronomy) + "\n"
                # informazioni meteorologiche ogni ora
                for hourly in forecast.hourly:
                    # preleva informazioni solo della giornata attuale
                    if is_current_forecast:
                        # preleva le informazioni meteorologiche riguardante le percentuali
                        if datetime.now().hour >= (hourly.time / 100):
                            remaining_hours_within_current_day += 1
                            chance_of_fog += hourly.chance_of_fog
                            chance_of_frost += hourly.chance_of_frost
                            chance_of_windy += hourly.chance_of_windy
                            chance_of_rain += hourly.chance_of_rain
                            chance_of_snow += hourly.chance_of_snow
                            chance_of_hightemp += hourly.chance_of_hightemp
                            chance_of_overcast += hourly.chance_of_overcast
                            chance_of_humidity += hourly.humidity
                            chance_of_thunder += hourly.chance_of_thunder
                    # preleva informazioni meteorologiche
                    if self.language == Language.ITALIANO.value:
                        forecast_three_days += f" --> ora: {hourly.time / 100} " \
                                               f"temperatura: {hourly.temperature}C° " \
                                               f"{hourly.description} {hourly.type} " \
                                               f"velocità vento: {hourly.wind_speed}Km/h " \
                                               f"direzione vento: {hourly.wind_direction!r}\n"
                    else:
                        forecast_three_days += f" --> hour: {hourly.time / 100} " \
                                               f"temperature: {hourly.temperature}C° " \
                                               f"{hourly.description} {hourly.type} " \
                                               f"wind speed: {hourly.wind_speed}Km/h " \
                                               f"wind direction: {hourly.wind_direction!r}\n"
                # previsione della giornata attuale letta
                is_current_forecast = False

            # normalizza le percentuali
            chance_of_frost /= remaining_hours_within_current_day
            chance_of_windy /= remaining_hours_within_current_day
            chance_of_rain /= remaining_hours_within_current_day
            chance_of_snow /= remaining_hours_within_current_day
            chance_of_hightemp /= remaining_hours_within_current_day
            chance_of_overcast /= remaining_hours_within_current_day
            chance_of_humidity /= remaining_hours_within_current_day
            chance_of_thunder /= remaining_hours_within_current_day

            # analisi delle percentuali
            other_info = ""
            # percentuali nuvole
            if 85 < chance_of_overcast < 100:
                other_info += MAX_OVERCAST_ITA if self.language == Language.ITALIANO.value else MAX_OVERCAST_ENG
            elif 65 < chance_of_overcast < 85:
                other_info += MORE_OVERCAST_ITA if self.language == Language.ITALIANO.value else MORE_OVERCAST_ENG
            elif 35 < chance_of_overcast < 65:
                other_info += ENOUGH_OVERCAST_ITA if self.language == Language.ITALIANO.value else ENOUGH_OVERCAST_ENG
            elif 15 < chance_of_overcast < 35:
                other_info += MIN_OVERCAST_ITA if self.language == Language.ITALIANO.value else MIN_OVERCAST_ENG
            else:
                other_info += NOTHING_OVERCAST_ITA if self.language == Language.ITALIANO.value else NOTHING_OVERCAST_ENG

            # percentuali temporali
            if 85 < chance_of_thunder < 100:
                other_info += MAX_THUNDER_ITA if self.language == Language.ITALIANO.value else MAX_THUNDER_ENG
            elif 65 < chance_of_thunder < 85:
                other_info += MORE_THUNDER_ITA if self.language == Language.ITALIANO.value else MORE_THUNDER_ENG
            elif 35 < chance_of_thunder < 65:
                other_info += ENOUGH_THUNDER_ITA if self.language == Language.ITALIANO.value else ENOUGH_THUNDER_ENG
            elif 15 < chance_of_thunder < 35:
                other_info += MIN_THUNDER_ITA if self.language == Language.ITALIANO.value else MIN_THUNDER_ENG
            else:
                other_info += NOTHING_THUNDER_ITA if self.language == Language.ITALIANO.value else NOTHING_THUNDER_ENG

            # percentuali pioggia e neve
            if chance_of_rain > chance_of_snow:
                if 85 < chance_of_rain < 100:
                    other_info += MAX_RAIN_ITA if self.language == Language.ITALIANO.value else MAX_RAIN_ENG
                elif 65 < chance_of_rain < 85:
                    other_info += MORE_RAIN_ITA if self.language == Language.ITALIANO.value else MORE_RAIN_ENG
                elif 35 < chance_of_rain < 65:
                    other_info += ENOUGH_RAIN_ITA if self.language == Language.ITALIANO.value else ENOUGH_RAIN_ENG
                elif 15 < chance_of_rain < 35:
                    other_info += MIN_RAIN_ITA if self.language == Language.ITALIANO.value else MIN_RAIN_ENG
                else:
                    other_info += NOTHING_RAIN_ITA if self.language == Language.ITALIANO.value else NOTHING_RAIN_ENG
            else:
                if 85 < chance_of_snow < 100:
                    other_info += MAX_SNOW_ITA if self.language == Language.ITALIANO.value else MAX_SNOW_ENG
                elif 65 < chance_of_snow < 85:
                    other_info += MORE_SNOW_ITA if self.language == Language.ITALIANO.value else MORE_SNOW_ENG
                elif 35 < chance_of_snow < 65:
                    other_info += ENOUGH_SNOW_ITA if self.language == Language.ITALIANO.value else ENOUGH_SNOW_ENG
                elif 15 < chance_of_snow < 35:
                    other_info += MIN_SNOW_ITA if self.language == Language.ITALIANO.value else MIN_SNOW_ENG
                else:
                    other_info += NOTHING_SNOW_ITA if self.language == Language.ITALIANO.value else NOTHING_SNOW_ENG

            # percentuali caldo e freddo
            if chance_of_hightemp > chance_of_frost:
                if chance_of_hightemp > 60:
                    other_info += MORE_HIGHTEMP_ITA if self.language == Language.ITALIANO.value else MORE_HIGHTEMP_ENG
                else:
                    other_info += MIN_HIGHTEMP_ITA if self.language == Language.ITALIANO.value else MIN_HIGHTEMP_ENG
            else:
                if chance_of_frost > 60:
                    other_info += MORE_FOREST_ITA if self.language == Language.ITALIANO.value else MORE_FOREST_ENG
                else:
                    other_info += MIN_FOREST_ITA if self.language == Language.ITALIANO.value else MIN_FOREST_ENG

            # percentuali percentuale vento
            if 85 < chance_of_windy < 100:
                other_info += MAX_WINDY_ITA if self.language == Language.ITALIANO.value else MAX_WINDY_ENG
            elif 65 < chance_of_windy < 85:
                other_info += MORE_WINDY_ITA if self.language == Language.ITALIANO.value else MORE_WINDY_ENG
            elif 35 < chance_of_windy < 65:
                other_info += ENOUGH_WINDY_ITA if self.language == Language.ITALIANO.value else ENOUGH_WINDY_ENG
            elif 15 < chance_of_windy < 35:
                other_info += MIN_WINDY_ITA if self.language == Language.ITALIANO.value else MIN_WINDY_ENG
            else:
                other_info += NOTHING_WINDY_ITA if self.language == Language.ITALIANO.value else NOTHING_WINDY_ENG

            # percentuali umidità
            if 85 < chance_of_humidity < 100:
                other_info += MAX_HUMIDITY_ITA if self.language == Language.ITALIANO.value else MAX_HUMIDITY_ENG
            elif 65 < chance_of_humidity < 85:
                other_info += MORE_HUMIDITY_ITA if self.language == Language.ITALIANO.value else MORE_HUMIDITY_ENG
            elif 35 < chance_of_humidity < 65:
                other_info += ENOUGH_HUMIDITY_ITA if self.language == Language.ITALIANO.value else ENOUGH_HUMIDITY_ENG
            elif 15 < chance_of_humidity < 35:
                other_info += MIN_HUMIDITY_ITA if self.language == Language.ITALIANO.value else MIN_HUMIDITY_ENG
            else:
                other_info += NOTHING_HUMIDITY_ITA if self.language == Language.ITALIANO.value else NOTHING_HUMIDITY_ENG

            # percentuali nebbia
            if 85 < chance_of_fog < 100:
                other_info += MAX_FOG_ITA if self.language == Language.ITALIANO.value else MAX_FOG_ENG
            elif 65 < chance_of_fog < 85:
                other_info += MORE_FOG_ITA if self.language == Language.ITALIANO.value else MORE_FOG_ENG
            elif 35 < chance_of_fog < 65:
                other_info += ENOUGH_FOG_ITA if self.language == Language.ITALIANO.value else ENOUGH_FOG_ENG
            elif 15 < chance_of_fog < 35:
                other_info += MIN_FOG_ITA if self.language == Language.ITALIANO.value else MIN_FOG_ENG
            else:
                other_info += NOTHING_FOG_ITA if self.language == Language.ITALIANO.value else NOTHING_FOG_ENG

            # stampa le previsioni dei 3 giorni
            print(city + "\n" + forecast_three_days)

            # ritorna analisi delle percentuali riguardanti i fenomeni meteorologici della restante giornata
            return other_info

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

                # preleva other meteorological info
                other_info = get_other_info(city, weather)

                # ritorna informazioni meteorologiche e astronomiche della città

                return "Attualmente a " + city + " ci sono " + current_temperature + \
                       " gradi centigradi. " + other_info + \
                       " Ti mostro le previsioni nei prossimi 2 giorni e i dettagli astronomici." \
                    if self.language == Language.ITALIANO.value else \
                    "Currently at " + city + " there are " + current_temperature + \
                    " degrees centigrade. " + other_info + \
                    " I show you the forecast over the next 2 days and astronomical details."

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
            return CORRECT_MORNING_ITA if self.language == Language.ITALIANO.value else CORRECT_MORNING_ENG
        elif actually_is_afternoon:
            return CORRECT_AFTERNOON_ITA if self.language == Language.ITALIANO.value else CORRECT_AFTERNOON_ENG
        elif actually_is_evening:
            return CORRECT_EVENING_ITA if self.language == Language.ITALIANO.value else CORRECT_EVENING_ENG
        else:
            return CORRECT_NIGHT_ITA if self.language == Language.ITALIANO.value else CORRECT_NIGHT_ENG

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
