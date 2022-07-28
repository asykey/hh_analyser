import requests
from typing import Any


def get_vacancies(url, params: dict) -> Any:
    return requests.get(url, params=params).json()


def get_vacancy(url, vacancy_id: int) -> Any:
    return requests.get(url + '{}'.format(vacancy_id)).json()