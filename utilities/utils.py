import platform
from datetime import datetime

ONE = "uno" or "one"
TWO = "due" or "two"
THREE = "tre" or "three"
FOUR = "quattro" or "four"
FIVE = "cinque" or "five"
SIX = "sei" or "six"
SEVEN = "sette" or "seven"
EIGHT = "otto" or "eight"
NINE = "nove" or "nine"


def normalize(text):
    text_to_return = ""

    text = text.lower(). \
        replace("ì", "i'"). \
        replace("è", "e'"). \
        replace("é", "e'"). \
        replace("ò", "o'"). \
        replace("à", "a'"). \
        replace("ù", "u'"). \
        replace("pi greco", "3,14'"). \
        replace("eulero", "2,71'")

    for word in text:
        if word == ONE:
            text_to_return += "1"
        elif word == TWO:
            text_to_return += "2"
        elif word == THREE:
            text_to_return += "3"
        elif word == FOUR:
            text_to_return += "4"
        elif word == FIVE:
            text_to_return += "5"
        elif word == SIX:
            text_to_return += "6"
        elif word == SEVEN:
            text_to_return += "7"
        elif word == EIGHT:
            text_to_return += "8"
        elif word == NINE:
            text_to_return += "9"
        else:
            text_to_return += word

    return text_to_return


# preleva l'orario e rimuovi gli zeri superflui
current_time = datetime.now().strftime('%#H e %#M').replace(" e 0", "") \
    if platform.system() == "Windows" else \
    datetime.now().strftime('%-H e %-M').replace(" e 0", "")

# verifica parte della giornata
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
        cities = [normalize(row.replace("\n", "")) for row in f]
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
           request.__contains__("quanto") and request.__contains__("ne") and request.__contains__("abbiamo") or \
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


def plus_in(string):
    return any(word in string.replace("'", " ").split(" ") for word in
               ["+", "piu", "plus"])


def minus_in(string):
    return any(word in string.replace("'", " ").split(" ") for word in
               ["-", "meno", "minus"])


def for_in(string):
    return any(word in string.replace("'", " ").split(" ") for word in
               ["*", "x", "per", "moltiplicato", "times", "for", "multiplied"])


def divided_in(string):
    return any(word in string.replace("'", " ").split(" ") for word in
               ["/", "diviso", "fratto", "divided", "fraction"])


def elevated_in(string):
    return any(word in string.replace("'", " ").split(" ") for word in
               ["elevato", "power", "elevato", "al", "alla", "elevated", "power"])


def logarithm_in(string):
    return any(word in string.replace("'", " ").split(" ") for word in
               ["logaritmo", "logarithm"])


def base_in(string):
    return any(word in string.replace("'", " ").split(" ") for word in
               ["base"])


def factorial_in(string):
    return any(word in string.replace("'", " ").split(" ") for word in
               ["fattoriale", "factorial"])


def root_in(string):
    return any(word in string.replace("'", " ").split(" ") for word in
               ["radice", "root"])


def index_in(string):
    return any(word in string.replace("'", " ").split(" ") for word in
               ["indice", "index"])


def operator_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["+", "-", "*", "x", "/", "piu", "meno", "per", "moltiplicato", "diviso", "fratto",
                "elevato", "potenza", "al", "alla", "radice", "indice", "logaritmo", "base", "fattoriale",
                "plus", "minus", "times", "for", "multiplied", "divided", "fraction",
                "elevated", "power", "root", "index", "logarithm", "base", "factorial"])


def one_cardinal_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["prima", "first"])


def two_cardinal_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["seconda", "quadrato", "second", "square"])


def three_cardinal_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["terza", "cubo", "cubica", "third", "cube", "cubic"])


def four_cardinal_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["quarta", "fourth"])


def five_cardinal_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["quinta", "fifth"])


def six_cardinal_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["sesta", "sixth"])


def seven_cardinal_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["settima", "seventh"])


def eight_cardinal_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["ottava", "eighth"])


def nine_cardinal_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["nona", "ninth"])


def ten_cardinal_in(request):
    return any(word in request.replace("'", " ").split(" ") for word in
               ["decima", "tenth"])


def cardinal_number_in(request):
    return one_cardinal_in(request) or \
           two_cardinal_in(request) or \
           three_cardinal_in(request) or \
           four_cardinal_in(request) or \
           five_cardinal_in(request) or \
           six_cardinal_in(request) or \
           seven_cardinal_in(request) or \
           eight_cardinal_in(request) or \
           nine_cardinal_in(request) or \
           ten_cardinal_in(request)


def number_in(request):
    return any(char.isdigit() for char in request)


def only_number_in(request):
    return all(char.isdigit() for char in request)


def know_calculations_from(request):
    return operator_in(request) and number_in(request)


KNOWLEDGE = "./db.sqlite3"
MODEL_ITA = "./models/modello_italiano"
MODEL_ENG = "./models/modello_inglese"
REC_AUDIO = "./rec_audio.wav"
CITIES_CSV = "./utilities/cities.csv"
TRAINING_CONVERSATION_ITA = "./example_of_communication/comunicazione_di_addestramento"
TRAINING_CONVERSATION_ENG = "./example_of_communication/training_communication"

CHECK_MICROPHONE_ITA = "Controllare se il microfono è acceso, per favore."
CHECK_MICROPHONE_ENG = "Please check if the microphone is on."

DOWNLOAD_MODEL_ITA = "Scaricare il modello da:\n" \
                     "https://alphacephei.com/vosk/models e decomprimere nella cartella models."
DOWNLOAD_MODEL_ENG = "Scaricare il modello da:\n" \
                     "https://alphacephei.com/vosk/models e decomprimere nella cartella models."

LISTENING_ITA = "In ascolto..."
LISTENING_ENG = "Listening..."

RECOGNITION_ITA = "Inizio del riconoscimento vocale..."
RECOGNITION_ENG = "Start of voice recognition..."

VERIFIED_A_PROBLEM_ITA = "Si e' verificato un problema! Riprova piu' tardi."
VERIFIED_A_PROBLEM_ENG = "A problem has occurred! Please try again later."

EXIT_ITA = "Va bene. A presto!"
EXIT_ENG = "All right. See you soon!"

TIME_ITA = f"Sono le ore: {current_time}" + \
           (" del mattino" if actually_is_morning else "") + \
           (" del pomeriggio" if actually_is_afternoon else "") + \
           (" di sera" if actually_is_evening else "") + \
           (" di node" if actually_is_night else "")
TIME_ENG = f"Are the hours: {current_time}" + \
           (" in the morning" if actually_is_morning else "") + \
           (" in the afternoon" if actually_is_afternoon else "") + \
           (" in the evening" if actually_is_evening else "") + \
           (" at night" if actually_is_night else "")

CITY_UNRECOGNIZED_ITA = "Mi spiace. Non ho capito il nome della città."
CITY_UNRECOGNIZED_ENG = "I'm sorry. I didn't get the name of the city."

CORRECT_MORNING_ITA = "Sono le " + str(datetime.now().hour) + " del mattino. Buon giorno!"
CORRECT_MORNING_ENG = "It is " + str(datetime.now().hour) + " in the morning. Good morning!"
CORRECT_AFTERNOON_ITA = "Sono le " + str(datetime.now().hour) + " del pomeriggio. Buon pomeriggio!"
CORRECT_AFTERNOON_ENG = "It is " + str(datetime.now().hour) + " in the afternoon. Good afternoon!"
CORRECT_EVENING_ITA = "Sono le " + str(datetime.now().hour) + " di sera. Buona sera!"
CORRECT_EVENING_ENG = "It is " + str(datetime.now().hour) + " in the evening. Good evening!"
CORRECT_NIGHT_ITA = "Sono le " + str(datetime.now().hour) + " di notte. Buona notte!"
CORRECT_NIGHT_ENG = "It is " + str(datetime.now().hour) + " at night. Good night!"

MAX_OVERCAST_ITA = "Il resto della giornata sara' nuvoloso "
MAX_OVERCAST_ENG = "The rest of the day will be cloudy "
MORE_OVERCAST_ITA = "Nuvoli sparse saranno presenti per il resto della giornata "
MORE_OVERCAST_ENG = "Scattered clouds will be present for the rest of the day "
ENOUGH_OVERCAST_ITA = "Nuvoli sparse potrebbero accompagnare il resto della giornata "
ENOUGH_OVERCAST_ENG = "Scattered clouds could accompany the rest of the day "
MIN_OVERCAST_ITA = "Il resto della giornata sara' quasi sicuramente sereno "
MIN_OVERCAST_ENG = "The rest of the day will almost certainly be clear "
NOTHING_OVERCAST_ITA = "Il resto della giornata sara' sicuramente sereno "
NOTHING_OVERCAST_ENG = "The rest of the day will definitely be clear "

MAX_THUNDER_ITA = "con forti temporali. "
MAX_THUNDER_ENG = "with severe thunderstorms. "
MORE_THUNDER_ITA = "con temporali molto probabili. "
MORE_THUNDER_ENG = "with thunderstorms very likely. "
ENOUGH_THUNDER_ITA = "con presunti temporali. "
ENOUGH_THUNDER_ENG = "con presunti temporali. "
MIN_THUNDER_ITA = "quasi sicuramente senza temporali."
MIN_THUNDER_ENG = "The rest of the day will almost certainly be clear "
NOTHING_THUNDER_ITA = "senza temporali, perfetta per una passeggiata all'aria aperta. "
NOTHING_THUNDER_ENG = "without thunderstorms, perfect for a walk in the fresh air. "

MAX_RAIN_ITA = "In aggiunta, la giornata sara' caratterizzata da piogge incessanti. "
MAX_RAIN_ENG = "Also, the day will be characterized by incessant rains. "
MORE_RAIN_ITA = "C'è il rischio di piogge. "
MORE_RAIN_ENG = "There is the risk of rainfall. "
ENOUGH_RAIN_ITA = "E' prevista pioggia."
ENOUGH_RAIN_ENG = "Rain is expected. "
MIN_RAIN_ITA = "Non dovrebbero esserci piogge. "
MIN_RAIN_ENG = "There should be no rain. "
NOTHING_RAIN_ITA = "Il rischio di pioggia e' esiguo. "
NOTHING_RAIN_ENG = "The risk of rain is small. "

MAX_SNOW_ITA = "In aggiunta, la giornata sara' caratterizzata da neve incessante. "
MAX_SNOW_ENG = "In addition, the day will feature unrelenting snow. "
MORE_SNOW_ITA = "C'è rischio di neve. "
MORE_SNOW_ENG = "There is the risk of snow. "
ENOUGH_SNOW_ITA = "E' prevista neve. "
ENOUGH_SNOW_ENG = "Snow is expected. "
MIN_SNOW_ITA = "Non dovrebbe esserci neve. "
MIN_SNOW_ENG = "There should be no snow. "
NOTHING_SNOW_ITA = "Il rischio di neve e' esiguo. "
NOTHING_SNOW_ENG = "The risk of snow is small. "

MORE_HIGHTEMP_ITA = "Il clima e' per lo piu' caldo, "
MORE_HIGHTEMP_ENG = "The climate is mostly warm, "
MIN_HIGHTEMP_ITA = "Il clima e' mite, "
MIN_HIGHTEMP_ENG = "The climate is mild, "

MORE_FOREST_ITA = "Il clima e' per lo piu' freddo, "
MORE_FOREST_ENG = "The climate is mostly cold, "
MIN_FOREST_ITA = "Il clima e' freschetto, "
MIN_FOREST_ENG = "The weather is cool, "

MAX_WINDY_ITA = "con forti venti, "
MAX_WINDY_ENG = "with strong winds, "
MORE_WINDY_ITA = "con venti insistenti, "
MORE_WINDY_ENG = "with persistent winds, "
ENOUGH_WINDY_ITA = "ventoso, "
ENOUGH_WINDY_ENG = "windy, "
MIN_WINDY_ITA = "con venticelli, "
MIN_WINDY_ENG = "with breezes, "
NOTHING_WINDY_ITA = "per niente ventoso, "
NOTHING_WINDY_ENG = "not at all windy, "

MAX_HUMIDITY_ITA = "molto umido e "
MAX_HUMIDITY_ENG = "very wet and "
MORE_HUMIDITY_ITA = "abbastanza umido e "
MORE_HUMIDITY_ENG = "quite moist and "
ENOUGH_HUMIDITY_ITA = "un po' umido e "
ENOUGH_HUMIDITY_ENG = "a little damp and "
MIN_HUMIDITY_ITA = "con scarsissima umidita' e "
MIN_HUMIDITY_ENG = "with very low humidity and "
NOTHING_HUMIDITY_ITA = "per niente umido e "
NOTHING_HUMIDITY_ENG = "not at all moist and "

MAX_FOG_ITA = "heavily foggy"
MAX_FOG_ENG = "fortemente nebbioso"
MORE_FOG_ITA = "con nebbie fitte."
MORE_FOG_ENG = "with thick mists."
ENOUGH_FOG_ITA = "con una leggera nebbia."
ENOUGH_FOG_ENG = "with a light mist."
MIN_FOG_ITA = "con nebbie scarse."
MIN_FOG_ENG = "with scanty mists."
NOTHING_FOG_ITA = "senza nebbia."
NOTHING_FOG_ENG = "without fog."

INCOMPREHENSIBLE_CALCULATION_ITA = "Non sono stato in grado di comprendere il calcolo richiesto. Prova altre parole."
INCOMPREHENSIBLE_CALCULATION_ENG = "I was unable to understand the required calculation. Try other words."
