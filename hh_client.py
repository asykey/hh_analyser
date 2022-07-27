import requests
from typing import Any


def get_vacancies(url, params: dict) -> Any:
    return requests.get(url, params=params).json()


def get_vacancy(url, vacancy_id: int) -> Any:
    return requests.get(url + '{}'.format(vacancy_id)).json()


def get_pages_count(url, params: dict) -> int:
    response = requests.get(url, params=params).json()
    return response["pages"]