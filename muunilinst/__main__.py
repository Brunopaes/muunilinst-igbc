import os

from handlers import analyst_endpoint


def main():
    """Exposes the application endpoints."""
    analyst_endpoint.app.run()


if __name__ == '__main__':
    main()
