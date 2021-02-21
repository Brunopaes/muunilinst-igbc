# -*- coding: utf-8 -*-
import helpers
import tweepy


class PS5StockAlerts:
    def __init__(self, user='PS5StockAlerts', limit=1, verbose=True):
        self.credentials = helpers.read_json('settings/ps_settings.json')

        self.api = tweepy.API(self.authenticate())

        self.user = user
        self.limit = limit
        self.verbose = verbose

        self.chat_list = [result[0] for result in self.querying()]

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
    def querying():
        helpers.set_path()
        return helpers.start_connection().query("""
            SELECT
                DISTINCT(CHAT_ID)
            FROM
                `mooncake-304003.misc.ps5-stock`

        """)

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
        )[0]

    # Used in __call__
    @staticmethod
    def seek_and_destroy(tweet, verbose):
        """This function seeks for "Playstation 5 In Stock NOW"

        Parameters
        ----------
        tweet : tweepy.models.Status.
            Latest tweet.
        verbose : bool
            Not found verbose.

        Returns
        -------
        url : str
            Tweet url.

        """
        if 'in stock now' in tweet.full_text.lower():
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
                helpers.courier(
                    url,
                    chat
                )

    def __call__(self, *args, **kwargs):
        self.telegram(self.seek_and_destroy(
            self.retrieve_tweets(), self.verbose),
            self.chat_list
        )


if __name__ == '__main__':
    PS5StockAlerts(verbose=False).__call__()
