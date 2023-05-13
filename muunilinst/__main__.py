import os

from handlers import market_analyst_edp, aggregator_edp


def main():
    """Exposes the application endpoints."""
    aggregator_edp.handler.run()


if __name__ == '__main__':
    main()
