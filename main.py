from FileWriter import FileWriter
import hh_client
import currency_client
import config
import vacancy_service
import analyser

import sys


def main():
    if len(sys.argv) < 2:
        raise RuntimeError("Необходимо передать строку поиска!")

    params = {
        'text': sys.argv[1],
        'page': 0,
        'per_page': 100,
        'schedule': 'remote',
        'only_with_salary': True
    }

    response = hh_client.get_vacancies(config.VACANCIES_URL, params)

    total = response["found"]

    vacancy_writer = FileWriter('vacancies.csv')
    vacancy_writer.set_fields(['id', 'name', 'salary', 'url'])

    skills_writer = FileWriter('skills.csv')
    skills_writer.set_fields(['id', 'skill'])

    currencies = currency_client.get_currencies(config.CBR_URL)

    begin = 0
    end = response["pages"]
    while begin <= end:
        params.update({'page': begin})
        vacancies = hh_client.get_vacancies(config.VACANCIES_URL, params)
        for item in vacancies["items"]:
            vacancy = hh_client.get_vacancy(config.VACANCIES_URL, item["id"])
            vacancy_data = vacancy_service.get_vacancy_data(vacancy)
            if vacancy_data["currency"] != "RUR":
                vacancy_data["salary"] = vacancy_data["salary"] * currencies[vacancy_data["currency"]]
            del vacancy_data["currency"]
            vacancy_writer.write_data(vacancy_data)
            vacancy_skills = vacancy_service.get_vacancy_skills(item["id"], vacancy["key_skills"])
            for skill in vacancy_skills:
                skills_writer.write_data(skill)
        begin = begin + 1

    print('Всего найдено {} вакансий'.format(total))
    skills = analyser.get_skills('skills.csv')
    print("Наиболее часто встречающиеся смежные навыки:")
    print(skills)
    salary_data = analyser.get_salaries_info('vacancies.csv')
    print('Зарплатные данные по запросу:')
    print('Максимальная зарплата: {}'.format(salary_data["max"]))
    print('Минимальная зарплата: {}'.format(salary_data["min"]))
    print('Средняя зарплата: {}'.format(salary_data["mean"]))


if __name__ == '__main__':
    main()
