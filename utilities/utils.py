from datetime import datetime

actually_is_morning = 5 <= datetime.now().hour < 12
actually_is_afternoon = 12 <= datetime.now().hour < 17
actually_is_evening = 17 <= datetime.now().hour < 22
actually_is_night = datetime.now().hour >= 22 or datetime.now().hour < 5


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


def exit_from(request):
    return any(word in request.split(" ") for word in
               ["esci", "spegniti", "exit", "turn off", "switch off"])


def know_name_bot_from(request):
    return request.__contains__("tuo nome") or \
           (request.__contains__("come") and request.__contains__("chiami")) or \
           (request.__contains__("che") and request.__contains__("nome")) or \
           request.__contains__("chiamarti") or \
           request.__contains__("your name") or \
           (request.__contains__("what") and request.__contains__("name")) or \
           request.__contains__("call you")


def know_time_from(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["ore", "ora", "orario", "hours", "hour"]) or \
           request.__contains__("what") and request.__contains__("time")


def know_date_from(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["data", "mese", "anno", "date", "day", "month", "year"]) or \
           request.__contains__("quale") and request.__contains__("giorno") or \
           request.__contains__("qual") and request.__contains__("giorno") or \
           request.__contains__("che") and request.__contains__("giorno") or \
           request.__contains__("giorno") and request.__contains__("oggi") or \
           request.__contains__("giorno") and request.__contains__("adesso") or \
           request.__contains__("quale") and request.__contains__("mese") or \
           request.__contains__("qual") and request.__contains__("mese") or \
           request.__contains__("che") and request.__contains__("mese") or \
           request.__contains__("mese") and request.__contains__("oggi") or \
           request.__contains__("mese") and request.__contains__("adesso") or \
           request.__contains__("quale") and request.__contains__("anno") or \
           request.__contains__("qual") and request.__contains__("anno") or \
           request.__contains__("che") and request.__contains__("anno") or \
           request.__contains__("anno") and request.__contains__("oggi") or \
           request.__contains__("anno") and request.__contains__("adesso")


def know_weather_from(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["meteo", "meteorologiche", "weather", "forecast"]) or \
           request.__contains__("previsioni") and request.__contains__("tempo") or \
           request.__contains__("come") and request.__contains__("tempo") or \
           request.__contains__("com") and request.__contains__("tempo") or \
           request.__contains__("quale") and request.__contains__("tempo") or \
           request.__contains__("qual") and request.__contains__("tempo") or \
           request.__contains__("che") and request.__contains__("tempo") or \
           request.__contains__("tempo") and request.__contains__("a") or \
           request.__contains__("tempo") and request.__contains__("di")
