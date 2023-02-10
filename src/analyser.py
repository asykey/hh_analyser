import pandas as pd


def get_skills(filename: str):
    data = pd.read_csv(filename, delimiter=';')
    return data.groupby(['skill']).size().sort_values(ascending=False).head(10)


def get_salaries_info(filename: str) -> dict:
    data = pd.read_csv(filename, delimiter=';')
    result = {
        'median': round(data['salary'].median()),
        'min': round(data['salary'].min()),
        'max': round(data['salary'].max())
    }
    return result


def get_total_vacancies(filename: str) -> int:
    data = pd.read_csv(filename, delimiter=';')
    return data.count()[0]
