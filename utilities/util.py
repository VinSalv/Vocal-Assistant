from datetime import datetime

MORNING = 5 <= datetime.now().hour < 12
AFTERNOON = 12 <= datetime.now().hour < 17
EVENING = 17 <= datetime.now().hour < 22
NIGHT = datetime.now().hour >= 22 or datetime.now().hour < 5


def greet_morning_in(string):
    return string.__contains__("buon giorno") or string.__contains__("buongiorno") or \
           string.__contains__("good morning") or string.__contains__("goodmorning")


def greet_afternoon_in(string):
    return string.__contains__("buon pomeriggio") or string.__contains__("buonpomeriggio") or \
           string.__contains__("good afternoon") or string.__contains__("goodafternoon")


def greet_evening_in(string):
    return string.__contains__("buona sera") or string.__contains__("buonasera") or \
           string.__contains__("good evening") or string.__contains__("goodevening")


def greet_night_in(string):
    return string.__contains__("buona notte") or string.__contains__("buonanotte") or \
           string.__contains__("good night") or string.__contains__("goodnight")


def extract_cities_from(csv):
    with open(csv, encoding="utf8") as f:
        cities = [row.lower().replace("\n", "") for row in f]
    return cities
