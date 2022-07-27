def get_vacancy_data(data: dict) -> dict:
    result = {
        "id": data["id"],
        "name": data["name"],
        "salary": data["salary"]["from"] if data["salary"]["to"] is None else
        data["salary"]["to"] if data["salary"]["from"] is None else
        (data["salary"]["from"] + data["salary"]["to"]) / 2,
        "currency": data["salary"]["currency"],
        "url": data["alternate_url"]
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
