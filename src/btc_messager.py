# -*- coding: utf-8 -*-
import datetime
import helpers


class BTCAdvisor:
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

    def fill_date_times(self):
        for date_time in (1, 5, 12):
            self.date_times.append(
                self.now - datetime.timedelta(hours=date_time)
            )

    def fill_values(self):
        for date_time in self.date_times:
            self.values.append([
                date_time.year,
                date_time.month,
                date_time.day,
                date_time.hour,
            ])

    def querying(self, operation):
        query_result = []
        for value in self.values:
            query_result.append([i for i in self.client.query(
                self.query.get(operation).format(
                    value[0], value[1], value[2], value[3]
                ))][0].values()[1])

        result = []
        for i in query_result:
            result.append(((query_result[0] / i) - 1) * 100)

        return result

    def checking_results(self, operation, operation_prices, value_min,
                         value_max):
        if operation == 'buy':
            if any([(elem <= value_min) or (elem <= value_max)
                    for elem in operation_prices]):
                true_values = [i for i, x in enumerate(
                    [(elem <= value_min) or (elem <= value_max)
                     for elem in operation_prices]) if x]

                for true_value in true_values:
                    self.message += 'Variação em {} de {}: {:.2f}\n'.format(
                        self.index.get(true_value),
                        self.operation.get(operation),
                        operation_prices[true_value]
                    )
        elif operation == 'sell':
            if any([(elem >= value_min) or (elem >= value_max)
                    for elem in operation_prices]):
                true_values = [i for i, x in enumerate(
                    [(elem >= value_min) or (elem >= value_max)
                     for elem in operation_prices]) if x]

                for true_value in true_values:
                    self.message += 'Variação em {} de {}: {:.2f}\n'.format(
                        self.index.get(true_value),
                        self.operation.get(operation),
                        operation_prices[true_value]
                    )

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
    BTCAdvisor().__call__()
