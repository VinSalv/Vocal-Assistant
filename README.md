# Vocal-Assistant

Implementation of Vocal Assisistant using google's speach recognition online/offline and ChatterBot's libraries.

## Paths
```
|-- Vocal Assistant
|   |-- bot
|   |   |-- Bot.py
|   |   |-- VoiceAndRecognition.py
|   |-- example_of_communication
|   |   |-- comunicazione_di_addestramento
|   |   |-- training_communication
|   |-- models
|   |   |-- modello_inglese
|   |   |-- modello_italiano
|   |-- db.sqlite3
|   |-- main.py
```

The developed code is divided in the following folders/classes:
-	The “bot” folder contains:
    -	Bot.py implementing class Bot related to ChatterBot which supports a communication and recognises specific commands;
    -	VoiceAssistant.py implementing the voice and the recognition capabvility related to the bot.
-	The “example_of_communication” folder contains text files to train the bot with an example of communication.
-	The “models” folder contains files to recognice the voce offline.
-	The file db.sqlite3 contains your interaction with the bot in order to improve its comunication.
-	The class main.py which allows to initialize and start the bot.

## Biography
ChatterBot: https://chatterbot.readthedocs.io/en/stable/
Voice and Recognition: https://geekitbase.info/content/8261
