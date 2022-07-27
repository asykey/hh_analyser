import pandas as pd


def get_skills(filename: str):
    data = pd.read_csv(filename, delimiter=';')
    return data.groupby(['skill']).size().sort_values(ascending=False).head(10)


def get_salaries_info(filename: str) -> dict:
    data = pd.read_csv(filename, delimiter=';')
    result = {
        'mean': data['salary'].mean(),
        'min': data['salary'].min(),
        'max': data['salary'].max()
    }
    return result
