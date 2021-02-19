# -*- coding: utf-8 -*-
import datetime
import helpers


class BTCourier:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.date_times = [self.now]
        self.values = []

        self.query = {
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
                    `mooncake-304003.DS_Bruno.btc-trader`)
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
                     `mooncake-304003.DS_Bruno.btc-trader`)
                 WHERE
                   OPERATION = "sell"
                   AND YEAR = {}
                   AND MONTH = {}
                   AND DAY = {}
                   AND HOUR = {}
                 ORDER BY
                   DATETIME DESC
             """
        }

        self.client = None

        self.results = {
            'buy': [],
            'sell': []
        }

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

        self.fill_date_times()

    # Used in __init__
    def fill_date_times(self):
        """This function calculates the datetime from 1, 5 and 12 hours ago.

        Returns
        -------

        """
        for date_time in (1, 5, 12):
            self.date_times.append(
                self.now - datetime.timedelta(hours=date_time)
            )

    # Used in __call__
    def fill_values(self):
        """This function updates a iterator with the date objects.

        Returns
        -------

        """
        for date_time in self.date_times:
            self.values.append([
                date_time.year,
                date_time.month,
                date_time.day,
                date_time.hour,
            ])

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
        return ((query_result[0] / result) - 1) * 100

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
        for value in self.values:
            query_result.append([i for i in self.client.query(
                self.query.get(operation).format(
                    value[0], value[1], value[2], value[3]
                ))][0].values()[1])

        result = []
        for result in query_result:
            result.append(self.calculus_methodology(query_result, result))

        return result

    # Used in __call__
    def checking_results(self, operation, operation_prices, bottom, top):
        """This function checks query's result.

        Parameters
        ----------
        operation : str
            Operation. buy or sell.
        operation_prices : iterator
            Operation prices - 1, 5 and 12 hour variation values.
        bottom : float
            Minimum value to trigger.
        top : float
            Maximum value to trigger.

        Returns
        -------

        """
        if operation == 'buy':
            if any([(elem <= bottom) or (elem <= top)
                    for elem in operation_prices]):
                true_values = [i for i, x in enumerate(
                    [(elem <= bottom) or (elem <= top)
                     for elem in operation_prices]) if x]

                for true_value in true_values:
                    self.message += 'Variação em {} de {}: {:.2f}\n'.format(
                        self.index.get(true_value),
                        self.operation.get(operation),
                        operation_prices[true_value]
                    )
        elif operation == 'sell':
            if any([(elem >= bottom) or (elem >= top)
                    for elem in operation_prices]):
                true_values = [i for i, x in enumerate(
                    [(elem >= bottom) or (elem >= top)
                     for elem in operation_prices]) if x]

                for true_value in true_values:
                    self.message += 'Variação em {} de {}: {:.2f}\n'.format(
                        self.index.get(true_value),
                        self.operation.get(operation),
                        operation_prices[true_value]
                    )

    # Used in __call__
    def __call__(self, *args, **kwargs):
        helpers.set_path()
        self.client = helpers.start_connection()

        self.fill_values()

        for operation, value_min, value_max in \
                zip(('buy', 'sell'), (-10, 5), (-5, 10)):
            self.message = ''
            self.checking_results(
                operation, self.querying(operation), value_min, value_max
            )

            if self.message != '':
                helpers.courier(self.message)


if __name__ == '__main__':
    BTCourier().__call__()
