"""
This will populate the initial data into convertion table.
File contains 6 columns:
    State
    Currency
    Symbol
    ISO Code
    Fractional Unit
    Variance (this is empty)
"""

import psycopg2
import requests
from bs4 import BeautifulSoup
from create_tables_manual import user, password, port, host, database


def get_currency_date(currencies):
    url_string = 'https://www.google.com/search?client=ubuntu&channel=fs&q='
    url_string += currencies
    url_string += '+to+USD&ie=utf-8&oe=utf-8'
    page = requests.get(url_string)

    result = set()
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        div = soup.find_all(class_='BNeawe iBp4i AP7Wnd')

        for val in div:
            result.add(val.text.split()[0])
        # BNeawe iBp4i AP7Wnd

    if len(result):
        return max(result)
    else:
        return None


if __name__ == '__main__':

    db = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(host, database, user,
                                                                                 password, port))

    cur = db.cursor()

    filename = 'currencies'
    count = 0

    with open(filename) as ff:
        lines = ff.readlines()
        print("Total lines: ", len(lines))

        for line in lines:
            values = line.split(',')
            currency = values[3]
            if values[-1]:
                values[-1] = ""

            rate = get_currency_date(currency)
            if rate:
                count += 1
            else:
                rate = 0

            insert_query = """insert into convertion(state, currency, symbol, iso_code,
            fractional_unit, variance)values (
            '{}', '{}', '{}', '{}', '{}', {})""".format(values[0].replace("'", ""), values[1], values[2],
                                                        values[3], values[4], rate)

            cur.execute(insert_query)
            print(line[:-1], "-", rate)

        db.commit()

        print("Currencies updated:", count)
