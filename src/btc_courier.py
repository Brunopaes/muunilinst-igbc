# -*- coding: utf-8 -*-
import datetime
import helpers


class BTCourier:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.date_times = self.fill_date_times()

        self.queries = {
            'buy': """
                SELECT
                    *
                FROM (
                    SELECT
                        OPERATION,
                        PRICE,
                        DATETIME,
                        EXTRACT(YEAR FROM DATETIME) AS YEAR,
                        EXTRACT(MONTH FROM DATETIME) AS MONTH,
                        EXTRACT(DAY FROM DATETIME) AS DAY,
                        EXTRACT(HOUR FROM DATETIME) AS HOUR,
                  FROM
                    `mooncake-304003.DS_Bruno.btc-historical`)
                WHERE
                  OPERATION = "buy"
                  AND YEAR = {}
                  AND MONTH = {}
                  AND DAY = {}
                  AND HOUR = {}
                ORDER BY
                  DATETIME DESC
            """,
            'sell': """
                SELECT
                    *
                FROM (
                    SELECT
                        OPERATION,
                        PRICE,
                        DATETIME,
                        EXTRACT(YEAR FROM DATETIME) AS YEAR,
                        EXTRACT(MONTH FROM DATETIME) AS MONTH,
                        EXTRACT(DAY FROM DATETIME) AS DAY,
                        EXTRACT(HOUR FROM DATETIME) AS HOUR,
                  FROM
                    `mooncake-304003.DS_Bruno.btc-historical`)
                WHERE
                  OPERATION = "sell"
                  AND YEAR = {}
                  AND MONTH = {}
                  AND DAY = {}
                  AND HOUR = {}
                ORDER BY
                  DATETIME DESC
            """,
            'bought_price': """
                SELECT 
                    *
                FROM 
                    `mooncake-304003.DS_Bruno.btc-trade`
                WHERE 
                    DATETIME = (
                        SELECT
                            MAX(DATETIME) AS DATETIME
                        FROM
                            `mooncake-304003.DS_Bruno.btc-trade`
                        WHERE
                            USERNAME = "{}"
                    )
            """,
            'fees': """
                SELECT
                    *
                FROM
                    `mooncake-304003.DS_Bruno.btc-fees`
            """
        }

        helpers.set_path()
        self.client = helpers.start_connection()

        self.date_values = self.fill_date_values()
        self.fees = self.fill_fees()

        self.message = ''

        self.index = {
            1: '1 hora',
            2: '5 horas',
            3: '12 horas',
        }

        self.operation = {
            'buy': 'Compra',
            'sell': 'Venda',
        }

        self.users = (
            'Bruno Paes',
            'Diego Tebet'
        )

        self.bought_prices = self.querying_bought_price()

    # Used in __init__
    def fill_date_times(self):
        """This function calculates the datetime from 1, 5 and 12 hours ago.

        Returns
        -------
        date_times: iterator
            Filled datetime list.

        """
        date_times = [self.now]
        for date_time in (1, 5, 12):
            date_times.append(
                self.now - datetime.timedelta(hours=date_time)
            )
        return date_times

    # Used in __init__
    def fill_date_values(self):
        """This function updates a iterator with the date objects.

        Returns
        -------
        values: iterator
            Filled values list.

        """
        values = []
        for date_time in self.date_times:
            values.append([
                date_time.year,
                date_time.month,
                date_time.day,
                date_time.hour,
            ])
        return values

    # Used in __init__
    def fill_fees(self):
        """This function creates a fees iterator.

        Returns
        -------
        fees: iterator
            Filled fees list.

        """
        return [j.values()[1:3] for j in
                [i for i in self.client.query(self.queries.get('fees'))]]

    # Used in __init__
    def querying_bought_price(self):
        """This functions queries user bought price.

        Returns
        -------
        bought_prices : iterator
            User bought prices.

        """
        bought_prices = []
        for user in self.users:
            try:
                bought_prices.append(
                    [i for i in self.client.query(self.queries.get(
                        'bought_price').format(user))][0].values()[2]
                )
            except IndexError:
                now = self.date_values[0]
                bought_prices.append([i for i in self.client.query(
                    self.queries.get('sell').format(
                        now[0], now[1], now[2], now[3]))][0].values()[1]
                )
        return bought_prices

    # Used in __call__
    def querying(self, operation):
        """This function queries into DL and calculates the hour 0 deviation.

        Parameters
        ----------
        operation : str
            Operation filter. buy or sell.

        Returns
        -------
        result : iterator
            Consolidated result's list.

        """
        query_result = []
        for value in self.date_values:
            query_result.append([i for i in self.client.query(
                self.queries.get(operation).format(
                    value[0], value[1], value[2], value[3]
                ))][0].values()[1])

        return query_result

    # Used in __call__
    def checking_results(self, operation, operation_prices):
        """This function checks query's result.

        Parameters
        ----------
        operation : str
            Operation. buy or sell.
        operation_prices : iterator
            Operation prices - 1, 5 and 12 hour variation values.

        Returns
        -------

        """
        if operation == 'buy':
            variation = []
            for result_ in operation_prices:
                variation.append(self.calculus_methodology(
                    operation_prices, result_
                ))
            if any([(elem <= self.fees[1][0]) or (elem <= self.fees[1][1])
                    for elem in variation]):
                true_values = [i for i, x in enumerate(
                    [(elem <= self.fees[1][0]) or (elem <= self.fees[1][1])
                     for elem in variation]) if x]

                for true_value in true_values:
                    self.message += 'Variação em {} de {}: {:.2f}\n'.format(
                        self.index.get(true_value),
                        self.operation.get(operation),
                        variation[true_value]
                    )
                self.message += '\n'
        elif operation == 'sell':
            for user_bought_price, user in zip(self.bought_prices, self.users):
                operation_prices[0] = user_bought_price

                variation = []
                for result_ in operation_prices:
                    variation.append(self.calculus_methodology(
                        operation_prices, result_
                    ))
                if any([(elem >= self.fees[0][0]) or (elem >= self.fees[0][1])
                        for elem in variation]):
                    true_values = [i for i, x in enumerate(
                        [(elem >= self.fees[0][0]) or (elem >= self.fees[0][1])
                         for elem in variation]) if x]

                    if len(true_values) > 0:
                        self.message += '{}:\n\n'.format(user)

                    for true_value in true_values:
                        self.message += 'Variação em {} de {}: {:.2f}\n'.format(
                            self.index.get(true_value),
                            self.operation.get(operation),
                            variation[true_value]
                        )
                    self.message += '\n'

    # Used in querying
    @staticmethod
    def calculus_methodology(query_result, result):
        """This function calculates the hour 0 deviation.

        Parameters
        ----------
        query_result : iterator
            The queried results.
        result : float
            1, 5 or 12 hour-shifted price.

        Returns
        -------

        """
        return ((result / query_result[0]) - 1) * 100

    # Used in __call__
    def __call__(self, *args, **kwargs):
        for operation in ('buy', 'sell'):
            self.message = ''
            self.checking_results(
                operation, self.querying(operation)
            )

            if self.message != '':
                helpers.courier(self.message)


if __name__ == '__main__':
    BTCourier().__call__()