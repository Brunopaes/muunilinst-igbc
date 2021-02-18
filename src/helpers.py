# -*- coding: utf-8 -*-
from google.cloud import bigquery

import telebot
import json
import os


def set_path():
    """This function sets settings.json in PATH.

    Returns
    -------

    """
    path = os.path.abspath('gcp-credentials.json')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path


def start_connection():
    """Function used to start connection with GCP's Big Query.

    Returns
    -------

    """
    return bigquery.Client()


def courier(message):
    bot = telebot.TeleBot(
        json.loads(open('settings.json', 'r').read())['API_TOKEN']
    )

    bot.send_message(-555674635, message)
