import requests
import pandas
from bs4 import BeautifulSoup


def requester():
    url = "https://coinmarketcap.com/new/"

    a = requests.get(
        url=url
    )

    data_dict = {}
    soup = BeautifulSoup(a.content, "html5lib")

    table = soup.find('table', {'class': 'sc-beb003d5-3 cJrmgS cmc-table'})
    header = {i: [] for i in [i.text for i in table.find_all('th')][2:-1]}

    body = table.find('tbody')

    for row in body.find_all('tr'):
        row_ = [i.text for i in row.find_all('td')][2:-1]
        for i, j in zip(header, row_):
            header.get(i).append(j)

    return header


if __name__ == '__main__':
    requester()