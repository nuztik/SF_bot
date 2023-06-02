import requests
import json

from config import *


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote_key}&from={base_key}&amount={amount}"
        payload = {}
        headers = {
            "apikey": API_KEY
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        resp = json.loads(response.content)
        new_price = resp ['result']
        return round(new_price, 2)
