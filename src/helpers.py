# -*- coding: utf-8 -*-
from google.cloud import bigquery

import telebot
import json
import os


def read_json(path):
    """This function opens a json file and parses it content into a python
    dict.

    Parameters
    ----------
    path : str
        The json file path.

    Returns
    -------
    json.load : dict
        The json content parsed into a python dict.

    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(e.args[-1])


def set_path():
    """This function sets telegram_settings.json in PATH.

    Returns
    -------

    """
    path = os.path.abspath('settings/gcp_settings.json')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path


def start_connection():
    """Function used to start connection with GCP's Big Query.

    Returns
    -------

    """
    return bigquery.Client()


def courier(message, chat_id=-555674635):
    """This function courier - through telegram bot - a message.

    Parameters
    ----------
    message : str
        To be couriered message.
    chat_id : int
        To be messaged chat id.

    Returns
    -------

    """
    telebot.TeleBot(**read_json('settings/telegram_settings.json'))\
        .send_message(chat_id, message)
