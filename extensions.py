import json
import requests

URL = 'https://api.coingate.com/v2/rates/merchant/{}/{}'
HELP_MESSAGE = """Привет, {}! Чтобы конвертировать валюту, напиши сообщение в следующем формате: 
<имя валюты> <имя валюты, в которую нужно перевести> 
<количество первой валюты>. Например, чтобы узнать, сколько в рублях будут стоить два с половиной евро, необходимо 
написать следующее: EUR RUB 2,5. Пользуйтесь аббревиатурами из трёх букв на английском языке для обозначения
 валюты. Сейчас доступны три валюты: Российский Рубль (RUB), Американский доллар (USD) и Евро (EUR)."""
POSSIBLE = ["RUB", "USD", "EUR"]


class BadRequest(BaseException):
    pass


class ConvertError(BaseException):
    pass


class Api:
    @staticmethod
    def get_price(base, quote, amount):
        base, quote = base.upper(), quote.upper()
        if base not in POSSIBLE or quote not in POSSIBLE:
            raise ConvertError("Укажите правильные сокращения валют. Подсказка: /help")
        amount = amount.replace(',', '.')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertError("Укажите количество валюты в формате числа. Подсказка: /help")
        r = requests.get(URL.format(base, quote))
        if not r.status_code == 200:
            raise BadRequest('Не удалось получить данные. Попробуйте ещё раз.')
        rate = json.loads(r.content)
        return f"{amount} {base} = {round(amount*rate, 2)} {quote}"

"""
У меня есть 120(amount) рублей(base) я хочу узнать сколько это в евро(quote)
нужно 120 умножить на курс евро к рублю AttributeError
"""
