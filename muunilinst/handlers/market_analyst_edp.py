import logging

import flask
from processors import market_analyst

logger = logging.Logger("Market Analyst", level=logging.INFO)

handler = flask.Flask(__name__)

config = {"market-analyst": {"requests": {
    "url": "https://coinmarketcap.com/new/"
}}}


@handler.route("/market-data", methods=["GET", "POST"])
def analyst_handler():
    logger.info("Request received in /market-data.")
    logger.info("Handling payload (requester).")
    request_config = config.get("market-analyst").get("requests", {})

    logger.info("Getting CoinMarketCap table.")
    response = market_analyst.requester(request_config)

    logger.info("Wrangling data.")
    return market_analyst.data_wrangler(response.content)
