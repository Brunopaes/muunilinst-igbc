# -*- coding: utf-8 -*-
from google.cloud import bigquery

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