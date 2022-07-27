import requests
import xmltodict


def get_currencies(url) -> dict:
    response = requests.get(url)
    courses = xmltodict.parse(response.content)
    result = {}
    for course in courses['ValCurs']["Valute"]:
        result.update({
            course["CharCode"]: float(course["Value"].replace(',', '.')) / int(course["Nominal"])
        })
    return result
