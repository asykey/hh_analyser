import requests
import xmltodict
from typing import Any


class CurrencyClient:
    def __init__(self):
        self.url = 'http://www.cbr.ru/scripts/XML_daily.asp'

    def get_currencies(self) -> dict:
        response = requests.get(self.url)
        courses = xmltodict.parse(response.content)
        result = {}
        for course in courses['ValCurs']["Valute"]:
            result.update({
                course["CharCode"]: course["Value"]
            })
        return result

