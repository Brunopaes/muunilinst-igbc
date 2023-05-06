from flask import Flask

from processors import get_data

app = Flask(__name__)


@app.route("/get-data")
def analyst_handler():
    return get_data.requester()
