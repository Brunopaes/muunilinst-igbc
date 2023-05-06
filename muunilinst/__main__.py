import os

from handlers import market_analyst_edp


def main():
    """Exposes the application endpoints."""
    market_analyst_edp.handler.run()


if __name__ == '__main__':
    main()
