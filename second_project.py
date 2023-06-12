import os
import sys
import json
import requests
import psycopg2
import datetime as dt
from datetime import date
from colorama import Fore
from dotenv import load_dotenv


load_dotenv()


class CurrencyConverter:
    def __init__(self, api_key, url_currency, url_history):
        self.api_key = api_key
        self.url_currency = url_currency
        self.url_history = url_history
        self.global_var = 0

    def create_server_connection(self):
        connection = None
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return connection

    def create_currency_table(self):
        cursor = self.connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS currency (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            base_currency VARCHAR(255),
            target_currency VARCHAR(255),
            conversion_rate FLOAT
            )
            '''
        cursor.execute(create_table_query)
        self.connection.commit()

    def insert_currency_data(
            self,
            timestamp,
            base_currency,
            target_currency,
            conversion_rate):
        cursor = self.connection.cursor()
        insert_query = '''
        INSERT INTO currency (timestamp, base_currency, target_currency, conversion_rate)
        VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(
            insert_query,
            (timestamp,
             base_currency,
             target_currency,
             conversion_rate))
        self.connection.commit()

    def convert_currency(self):
        time = dt.datetime.now()
        yesterday = time - dt.timedelta(days=1)
        yes_str = yesterday.strftime('%Y/%m/%d')

        while self.global_var < 1:
            try:
                currency = sys.stdin.readline().strip()
                if currency == "quit":
                    self.global_var += 1
                    break
                currency = currency.upper()
                words = currency.split(" ")
                if len(currency) == 7:
                    first_currency = words[0]
                    second_currency = words[1]
                    new_url = self.url_currency.replace("EUR", first_currency)
                    new_url = new_url.replace("GBP", second_currency)
                    new_url = new_url.replace("API_KEY", self.api_key)
                    response_currency = requests.get(new_url)
                    data_currency = response_currency.json()
                    for item in data_currency:
                        base_currency = data_currency["base_code"]
                        target_currency = data_currency["target_code"]
                        conversion = round(data_currency["conversion_rate"], 2)
                    new_url_history = self.url_history.replace(
                        "YEAR/MONTH/DAY", yes_str)
                    new_url_history = new_url_history.replace(
                        "USD", first_currency)
                    new_url_history = new_url_history.replace(
                        "API_KEY", self.api_key)
                    response_history = requests.get(new_url_history)
                    data_history = response_history.json()
                    for item_history in data_currency:
                        compare = round(
                            data_history["conversion_rates"][second_currency], 2)
                    if compare > conversion:
                        print(
                            time.strftime("%c"),
                            base_currency,
                            target_currency,
                            f"\033[1;31;49m{conversion}\033[0m"
                        )
                    else:
                        print(
                            time.strftime("%c"),
                            base_currency,
                            target_currency,
                            f"\033[1;32;49m{conversion}\033[0m"
                        )
                else:
                    print("Wrong input")
            except BaseException:
                print("Wrong input")


api_key = os.getenv("API_KEY")
url_currency = os.getenv("URL_CURRENCY")
url_history = os.getenv("URL_HISTORY")
converter = CurrencyConverter(api_key, url_currency, url_history)
converter.convert_currency()


def main():
    if __name__ == "__main__":
        main()
