import flask

handler = flask.Flask(__name__)


@handler.route("/")
def main_page():
    return "http://127.0.0.1:5000/aggregate\n"
