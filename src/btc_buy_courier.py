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
            'fees': """
                SELECT
                    *
                FROM
                    `mooncake-304003.DS_Bruno.btc-fees`
                WHERE 
                    OPERATION = "buy"
            """
        }
        helpers.set_path()
        self.client = helpers.start_connection()

        self.values = self.fill_date_values()
        self.fees = self.fill_fees().values()[1:3]

        self.results = {
            'buy': []
        }

        self.message = ''

        self.index = {
            1: '1 hora',
            2: '5 horas',
            3: '12 horas',
        }

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
        return [i for i in self.client.query(self.queries.get('fees'))][0]

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
                self.queries.get(operation).format(
                    value[0], value[1], value[2], value[3]
                ))][0].values()[1])

        result_ = []
        for result in query_result:
            result_.append(self.calculus_methodology(query_result, result))

        return result_

    # Used in __call__
    def checking_results(self,  operation_prices, bottom, top):
        """This function checks query's result.

        Parameters
        ----------
        operation_prices : iterator
            Operation prices - 1, 5 and 12 hour variation values.
        bottom : float
            Minimum value to trigger.
        top : float
            Maximum value to trigger.

        Returns
        -------

        """
        if any([(elem <= bottom) or (elem <= top)
                for elem in operation_prices]):
            true_values = [i for i, x in enumerate(
                [(elem <= bottom) or (elem <= top)
                 for elem in operation_prices]) if x]

            for true_value in true_values:
                self.message += 'Variação em Compra de {}: {:.2f}\n'.format(
                    self.index.get(true_value),
                    operation_prices[true_value]
                )

    # Used in __call__
    def __call__(self, *args, **kwargs):
        self.checking_results(
            self.querying('buy'), self.fees[0], self.fees[1]
        )

        if self.message != '':
            helpers.courier(self.message)


if __name__ == '__main__':
    BTCourier().__call__()
