# -*- coding: utf-8 -*-
import helpers
import tweepy


class PS5StockAlerts:
    def __init__(self, user='PS5StockAlerts', limit=5, verbose=True):
        self.credentials = helpers.read_json('settings/ps_settings.json')

        self.api = tweepy.API(self.authenticate())

        self.user = user
        self.limit = limit
        self.verbose = verbose

        self.queries = {
            'broadcast': """
                SELECT
                    DISTINCT(CHAT_ID)
                FROM
                    `mooncake-304003.misc.ps5-broadcast-list`
            """,
            'check_tweet': """
                SELECT
                    *
                FROM
                    `mooncake-304003.misc.processed-tweets`
            """,
            'insert_tweet': """
                INSERT INTO
                    `mooncake-304003.misc.processed-tweets`
                VALUES
                    ({})
            """
        }

        self.chat_list = [result[0] for result in self.querying(
            self.queries.get('broadcast'))]

    def authenticate(self):
        """This function authenticates into twitter.

        Returns
        -------
        auth : tweepy.auth.OAuthHandler
            Twitter authentication access.

        """
        auth = tweepy.OAuthHandler(**self.credentials.get('consumer'))
        auth.set_access_token(**self.credentials.get('application'))

        return auth

    # Used in __init__
    @staticmethod
    def querying(query):
        """This function queries into BQ.

        Parameters
        ----------
        query : str
            Query-string.

        Returns
        -------
        response : google.cloud.bigquery.job.query.QueryJob
            Query response.

        """
        helpers.set_path()
        return helpers.start_connection().query(query)

    # Used in __call__
    def retrieve_tweets(self):
        """This function retrieves the - latest - tweets from a given user.

        Returns
        -------
        response : tweepy.models.Status.
            Latest tweet.

        """
        return self.api.user_timeline(
            screen_name=self.user,
            count=self.limit,
            tweet_mode='extended'
        )

    # Used in seek_and_destroy
    def will_run(self, tweet_id):
        """This function checks if tweet was already processed.

        Parameters
        ----------
        tweet_id : int
            Tweet id.

        Returns
        -------

        """
        if tweet_id in [result[0] for result in self.querying(
                self.queries.get('check_tweet'))]:
            exit()
        self.querying(self.queries.get('insert_tweet').format(tweet_id))

    # Used in __call__
    def seek_and_destroy(self, tweets, verbose):
        """This function seeks for "Playstation 5 In Stock NOW"

        Parameters
        ----------
        tweets : iterator.
            Last 4 tweets.
        verbose : bool
            Not found verbose.

        Returns
        -------
        url : str
            Tweet url.

        """
        for tweet in tweets:
            if 'in stock now' in tweet.full_text.lower():
                self.will_run(tweet.id)
                return 'https://twitter.com/twitter/statuses/{}'.format(tweet.id)
        if verbose:
            return 'Impossible, perhaps the archives are incomplete!'

    # Used in __call__
    @staticmethod
    def telegram(url, chat_list):
        """This function sends message to chat list.

        Parameters
        ----------
        url : str
            Tweet url.
        chat_list : iterator
            Chat/User id list.

        Returns
        -------

        """
        if url is not None:
            for chat in chat_list:
                try:
                    helpers.courier(
                        url,
                        chat
                    )
                except helpers.telebot.apihelper.ApiTelegramException as e:
                    e.args

    def __call__(self, *args, **kwargs):
        self.telegram(self.seek_and_destroy(
            self.retrieve_tweets(), self.verbose),
            self.chat_list
        )


if __name__ == '__main__':
    PS5StockAlerts(verbose=False).__call__()
