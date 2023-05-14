from handlers import app, aggregator_edp, market_analyst_edp  # noqa: F401


def main():
    """Exposes the application endpoints."""
    app.handler.run(use_reloader=True)


if __name__ == "__main__":
    main()
