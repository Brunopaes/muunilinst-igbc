import logging
import flask

from processors import aggregator

logger = logging.Logger("Aggregator", level=logging.INFO)

handler = flask.Flask(__name__)


PAYLOAD_ = [
    {"key": {"tech": "hydro", "region": "aaa"}, "data": {"reference_date": "2023-01-01", "report_value": 10, "report_value_2": 1}},
    {"key": {"tech": "hydro", "region": "aaa"}, "data": {"reference_date": "2023-01-01", "report_value": 11, "report_value_2": 1}},
    {"key": {"tech": "hydro", "region": "aaa"}, "data": {"reference_date": "2023-01-02", "report_value": 12, "report_value_2": 1}},
    {"key": {"tech": "hydro", "region": "bbb"}, "data": {"reference_date": "2023-01-01", "report_value": 13, "report_value_2": 12}},
    {"key": {"tech": "hydro", "region": "bbb"}, "data": {"reference_date": "2023-01-02", "report_value": 13, "report_value_2": 12}},
]

KEYS_ = [
    {"key": "tech"},
    {"key": "region"},
    {"data": "reference_date"}
]

VALUES_ = ["report_value"]

AGGREGATION_TYPE_ = "sum"


@handler.route("/aggregate", methods=["GET", "POST"])
def aggregate_handler():
    return aggregator.aggregate(
        PAYLOAD_,
        KEYS_,
        VALUES_,
        AGGREGATION_TYPE_
    )
