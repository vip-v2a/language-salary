import requests
from itertools import count


def get_hhru_vacancies(text, area_id="1", period=30,
                       professional_role_id="96"):
    """Docstrings need

    """

    hhru_url = "https://api.hh.ru/vacancies"
    params = {
        "professional_role": professional_role_id,
        "area": area_id,
        "period": period,
        "search_field": "name",
        "text": text
    }

    for page in count(0):
        params["page"] = page
        hhru_response = requests.get(hhru_url, params)
        hhru_response.raise_for_status()
        hhru_data = hhru_response.json()

        if page >= hhru_data["pages"]:
            break

        yield from hhru_data["items"]


def predict_rub_salary(vacancy):

    if not (vacancy["salary"]
            and vacancy["salary"]["currency"] == "RUR"):
        return

    from_salary = vacancy["salary"]["from"]
    to_salary = vacancy["salary"]["to"]

    if not from_salary:
        return to_salary * 0.8
    if not to_salary:
        return from_salary * 1.2

    return 0.5 * (from_salary + to_salary)


def main():

    programming_languages = [
        "Python",
        "Java",
        "PHP",
        "JavaScript",
        "C++",
        "Swift",
        "Ruby",
        "Go",
        "React",
        "C#"
    ]
    salary_statistics = {}

    for language in programming_languages[:2]:

        salaries = []

        # hhru_response = get_hhru_response(language)
        # vacancies = hhru_response["items"]
        # vacancies = []

        for index, vacancy in enumerate(get_hhru_vacancies(language),
                                        start=1):
            salary = predict_rub_salary(vacancy)
            if salary:
                salaries.append(salary)
            print(language, index)

        salary_statistics[language] = {
            "vacancies_found": index,
            "vacancies_processed": len(salaries),
            "average_salary": int(sum(salaries)/len(salaries))
        }

    print(salary_statistics)


if __name__ == '__main__':
    main()
