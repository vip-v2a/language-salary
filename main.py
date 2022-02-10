import os
import logging
import requests
from itertools import count
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_hhru_vacancies(text, area_id="1", period=30,
                       professional_role_id="96"):

    url = "https://api.hh.ru/vacancies"
    params = {
        "professional_role": professional_role_id,
        "area": area_id,
        "period": period,
        "search_field": "name",
        "text": text
    }

    for page in count(0):
        params["page"] = page
        response = requests.get(url, params)
        response.raise_for_status()
        vacancies = response.json()

        yield vacancies["found"], vacancies["items"]

        if page + 1 >= vacancies["pages"]:
            break


def predict_rub_salary_hh(vacancy):

    salary = vacancy["salary"]

    if not (salary and salary["currency"] == "RUR"):
        return

    return predict_salary(
        salary_from=salary["from"],
        salary_to=salary["to"]
    )


def predict_salary(salary_from, salary_to):

    if not(salary_from or salary_to):
        return

    if not salary_from:
        return salary_to * 0.8
    if not salary_to:
        return salary_from * 1.2

    return 0.5 * (salary_from + salary_to)


def get_statistics_table(statistics, title):
    headers = [
        "Язык программирования",
        "Вакансий найдено",
        "Вакансий обработано",
        "Средняя зарплата"
    ]

    rows = [headers]

    for language, parameters in statistics.items():
        rows.append([language, *parameters.values()])

    table = AsciiTable(rows, title).table
    return table


def get_hhru_vacancy_statistics(programming_languages):

    statistics = {}

    for language in programming_languages:

        salaries = []

        for vacancies_found, vacancy in get_hhru_vacancies(language):
            salary = predict_rub_salary_hh(vacancy)
            if salary:
                salaries.append(salary)

        statistics[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(salaries),
            "average_salary": get_average_salary(salaries)
        }

    return statistics


def get_sj_vacancies(client_secret, keyword):

    url = "https://api.superjob.ru/2.0/vacancies/"

    headers = {
        "X-Api-App-Id": client_secret
    }

    params = {
        "town": 4,
        "catalogues": 48,
        "keyword": keyword,
        "count": 100
    }

    for page in count(0):
        params["page"] = page

        response = requests.get(
            url,
            params=params,
            headers=headers
        )
        response.raise_for_status()
        vacancies = response.json()

        yield from vacancies["objects"]

        if not vacancies["more"]:
            break


def get_sj_vacancy_statistics(programming_languages, client_secret):

    statistics = {}

    for language in programming_languages:

        index = 0
        salaries = []
        vacancies = get_sj_vacancies(client_secret, language)

        for index, vacancy in enumerate(vacancies, start=1):
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                salaries.append(salary)

        statistics[language] = {
            "vacancies_found": index,
            "vacancies_processed": len(salaries),
            "average_salary": get_average_salary(salaries)
        }

    return statistics


def get_average_salary(salaries):
    if not salaries:
        return 0
    return int(sum(salaries)/len(salaries))


def predict_rub_salary_sj(vacancy):
    if not vacancy["currency"] == "rub":
        return

    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]

    return predict_salary(salary_from, salary_to)


def main():

    logging.basicConfig(
        level=logging.WARNING,
        format="%(process)d %(levelname)s %(message)s"
    )

    load_dotenv()
    sj_api_key = os.getenv("SUPERJOB_API_KEY")

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

    hhru_salary_statistics = get_hhru_vacancy_statistics(
        programming_languages
    )

    sj_salary_statistics = get_sj_vacancy_statistics(
        programming_languages,
        sj_api_key,
    )

    hhru_table = get_statistics_table(
        hhru_salary_statistics,
        "HeadHunter Moscow"
    )

    sj_table = get_statistics_table(
        sj_salary_statistics,
        "SuperJob Moscow"
    )

    print(hhru_table)
    print(sj_table)


if __name__ == "__main__":
    main()
