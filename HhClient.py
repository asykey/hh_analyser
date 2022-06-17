import requests
from typing import Any


class HhClient:
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies/'

    def get_vacancies(self, params: dict) -> Any:
        return requests.get(self.url, params=params).json()

    def get_vacancy(self, vacancy_id: int) -> Any:
        return requests.get(self.url + '{}'.format(vacancy_id)).json()

    def get_pages_count(self, params: dict) -> int:
        response = requests.get(self.url, params=params).json()
        return response["pages"]