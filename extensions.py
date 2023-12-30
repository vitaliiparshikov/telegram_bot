import requests
import json

class APIException(Exception):
    def __init__(self, message):
        self.message = message

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        api_key = '6863738261:AAGER0HVzhWBYUR6oBjXVHoMRlYYRzSQ17c'

        r = f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}&api_key={api_key}'

        try:
            answer = requests.get(r)
            data = answer.json()

            if quote not in data:
                raise APIException(f"Данные по валюте {quote} отсутствуют в ответе API")

            conversion_rate = data[quote]

            result = float(amount) * conversion_rate
            return result

        except Exception as e:
            raise APIException(f"Ошибка при получении данных: {str(e)}")