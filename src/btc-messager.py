# -*- coding: utf-8 -*-
import helpers
import datetime


now = datetime.datetime.now()
one_hour = now - datetime.timedelta(hours=1)
five_hour = now - datetime.timedelta(hours=5)
ten_hour = now - datetime.timedelta(hours=12)

dict_ = {
    'year': [],
    'month': [],
    'day': [],
    'hour': []
}

year = now.year
month = now.month
day = now.day
hour = now.hour


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

query_result = [i for i in client.query(query.format(year, month, day, hour))]

now_value = query_result[0].values()[1]