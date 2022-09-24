# Vocal-Assistant

Implementation of Vocal Assistant using google's speach recognition online/offline and ChatterBot's libraries.

## Paths

```
|-- Vocal Assistant
|   |-- bot
|   |   |-- Bot.py
|   |   |-- Recognition.py
|   |   |-- Voice.py
|   |-- example_of_communication
|   |   |-- comunicazione_di_addestramento
|   |   |-- training_communication
|   |-- models
|   |   |-- modello_inglese
|   |   |-- modello_italiano
|   |-- utilities
|   |   |-- cities.csv
|   |   |-- Language.py
|   |   |-- util.py
|   |-- db.sqlite3
|   |-- main.py
```

The developed code is divided in the following folders/classes:

- The “bot” folder contains:
    - Bot.py implementing class Bot related to ChatterBot which sustains a conversation and performs carry out specific
      commands;
    - Recognition.py implementing the recognition capability related to the bot.
    - Voice.py implementing the voice related to the bot.
- The “example_of_communication” folder contains text files to train the bot with an example of communication.
- The “models” folder contains files to recognise the voce offline.
- The “utilities” folder contains:
    - cities.csv names of lots of cities;
    - Language.py implementing enumeration of italian and english language;
    - util.py implementing useful methods and constants;
- The file db.sqlite3 contains your interaction with the bot in order to improve its communication.
- The class main.py which allows to initialize and start the bot.

### Current capacities

- telling time
- telling date
- sustaining a simple conversation
- distinguish parts of day
- tell weather and forecast
- learning from interactions

## Biography

- ChatterBot: https://chatterbot.readthedocs.io/en/stable
- Voice and Recognition: https://geekitbase.info/content/8261
