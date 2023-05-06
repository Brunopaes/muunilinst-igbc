import requests

from bs4 import BeautifulSoup


def requester(config):
    return requests.get(**config)


def soup(response, parser: str = "html5lib"):
    return BeautifulSoup(response, parser)


def data_filtering(response_content):
    table = response_content.find(
        'table', {'class': 'sc-beb003d5-3 cJrmgS cmc-table'}
    ).find('tbody')

    data_dict = {}
    for row in table.find_all('tr'):
        row_ = [i.text for i in row.find_all('td')]
        data_dict.update({
            row_[2].split(row_[1])[1]: {
                "coin_name": row_[2].split(row_[1])[0],
                "blockchain": row_[8],
                "1_hour_performance": float(row_[4][:-1]),
                "24_hour_performance": float(row_[5][:-1]),
                "volume": float(row_[7][1:].replace(',', '')),
                "listing_time": row_[9][:-4]
            }
        })

    return data_dict


def data_wrangler(response_content):
    return data_filtering(
        soup(response_content)
    )
