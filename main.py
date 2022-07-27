from FileWriter import FileWriter
from HhClient import HhClient
from CurrencyClient import CurrencyClient

import sys
import pandas as pd

MAIN_URL = 'https://api.hh.ru/'


def get_vacancy_data(data: dict) -> dict:
    result = {
        "id": data["id"],
        "name": data["name"],
        "salary": data["salary"]["from"] if data["salary"]["to"] is None else
        data["salary"]["to"] if data["salary"]["from"] is None else
        calc_avg_salary(
            data["salary"]["from"], data["salary"]["to"]),
        "currency": data["salary"]["currency"]
    }
    return result


def get_vacancy_skills(vacancy_id: int, skills: list) -> list:
    result = []
    for skill in skills:
        result.append({
            "id": vacancy_id,
            "skill": skill["name"]
        })
    return result


def get_skills(filename: str):
    data = pd.read_csv(filename, delimiter=';')
    return data.groupby(['skill']).size().sort_values(ascending=False).head(10)


def calc_avg_salary(salary_from: int, salary_to: int) -> float:
    return (salary_from + salary_to) // 2


def get_salaries_info(filename: str) -> dict:
    data = pd.read_csv(filename, delimiter=';')
    result = {
        'mean': data['salary'].mean(),
        'min': data['salary'].min(),
        'max': data['salary'].max()
    }
    return result


def main():
    if len(sys.argv) < 2:
        raise RuntimeError("Необходимо передать строку поиска!")
    cc = CurrencyClient()
    currencies = cc.get_currencies()
    hh_client = HhClient()
    params = {
        'text': sys.argv[1],
        'page': 0,
        'per_page': 100,
        'schedule': 'remote',
        'only_with_salary': True
    }

    response = hh_client.get_vacancies(params)

    total = response["found"]

    vacancy_writer = FileWriter('vacancies.csv')
    vacancy_writer.set_fields(['id', 'name', 'salary', 'skills'])

    skills_writer = FileWriter('skills.csv')
    skills_writer.set_fields(['id', 'skill'])

    begin = 0
    end = response["pages"]
    while begin <= end:
        params.update({'page': begin})
        vacancies = hh_client.get_vacancies(params)
        for item in vacancies["items"]:
            vacancy = hh_client.get_vacancy(item["id"])
            vacancy_data = get_vacancy_data(vacancy)
            if vacancy_data["currency"] != "RUR":
                vacancy_data["salary"] = vacancy_data["salary"] * float(
                    currencies[vacancy_data["currency"]].replace(',', '.'))
            del vacancy_data["currency"]
            vacancy_writer.write_data(vacancy_data)
            vacancy_skills = get_vacancy_skills(item["id"], vacancy["key_skills"])
            for skill in vacancy_skills:
                skills_writer.write_data(skill)
        begin = begin + 1

    print('Всего найдено {} вакансий'.format(total))
    skills = get_skills('skills.csv')
    print("Наиболее часто встречающиеся смежные навыки:")
    print(skills)
    salary_data = get_salaries_info('vacancies.csv')
    print('Зарплатные данные по запросу:')
    print('Максимальная зарплата: {}'.format(salary_data["max"]))
    print('Минимальная зарплата: {}'.format(salary_data["min"]))
    print('Средняя зарплата: {}'.format(salary_data["mean"]))


if __name__ == '__main__':
    main()
