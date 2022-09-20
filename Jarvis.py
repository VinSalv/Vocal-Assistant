import logging

from chatterbot import ChatBot
from chatterbot.comparisons import levenshtein_distance
from chatterbot.response_selection import get_first_response
from chatterbot.trainers import ListTrainer

logging.basicConfig(level=logging.CRITICAL)


def setup_jarvis():
    bot = ChatBot(
        "Jarvis",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database="./db.sqlite3",
        logic_adapters=[
            "chatterbot.logic.BestMatch"
        ],
        statement_comparison_function=levenshtein_distance,
        response_selection_method=get_first_response
    )

    # addestramento con esempio di comunicazione
    with open("comunicazione_di_addestramento.txt") as f:
        conversation = f.readlines()
        trainer = ListTrainer(bot)
        trainer.train(conversation)

    return bot
