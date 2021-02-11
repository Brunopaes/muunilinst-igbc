# -*- coding: utf-8 -*-
import datetime
import helpers


now = datetime.datetime.now()
date_times = [now]
for date_time in (1, 5, 12):
    date_times.append(now - datetime.timedelta(hours=date_time))

values = []
for date_time in date_times:
    values.append([
        date_time.year,
        date_time.month,
        date_time.day,
        date_time.hour,
    ])


query = """
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
"""

helpers.set_path()
client = helpers.start_connection()

query_result = []
for value in values:
    query_result.append([i for i in client.query(query.format(
        value[0], value[1], value[2], value[3]
    ))][0].values()[1])

for i in query_result:
    print(((query_result[0] / i) - 1) * 100)
    print(query_result[0], i)
    print('--------')
