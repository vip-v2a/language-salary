import logging
import os
import requests
from itertools import count
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_hhru_vacancies(text, area_id="1", period=30,
                       professional_role_id="96"):

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
        hhru_vacancies = hhru_response.json()

        if page >= hhru_vacancies["pages"]:
            break

        yield from hhru_vacancies["items"]


def predict_rub_salary_hh(vacancy):

    if not (vacancy["salary"]
            and vacancy["salary"]["currency"] == "RUR"):
        return

    return predict_salary(
        salary_from=vacancy["salary"]["from"],
        salary_to=vacancy["salary"]["to"]
    )


def predict_salary(salary_from, salary_to):

    if not salary_from:
        return salary_to * 0.8
    if not salary_to:
        return salary_from * 1.2

    return 0.5 * (salary_from + salary_to)


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

    hhru_salary_statistics = {}
    sj_salary_statistics = {}

    hhru_salary_statistics = get_hhru_vacancy_statistics(
        programming_languages
    )

    sj_salary_statistics = get_sj_vacancy_statistics(
        programming_languages,
        sj_api_key,
    )

    display_statistics_table(hhru_salary_statistics, "HeadHunter Moscow")
    display_statistics_table(sj_salary_statistics, "SuperJob Moscow")


def display_statistics_table(statistics, title):
    headings = [
        "Язык программирования",
        "Вакансий найдено",
        "Вакансий обработано",
        "Средняя зарплата"
    ]

    rows = []
    rows.append(headings)

    for language, parameters in statistics.items():
        rows.append([language, *parameters.values()])

    table_instance = AsciiTable(rows, title)
    print(table_instance.table)


def get_hhru_vacancy_statistics(programming_languages):

    hhru_salary_statistics = {}

    for language in programming_languages:

        index = 0
        salaries = []
        vacancies = get_hhru_vacancies(language)

        for index, vacancy in enumerate(vacancies, start=1):
            salary = predict_rub_salary_hh(vacancy)
            if salary:
                salaries.append(salary)

        hhru_salary_statistics[language] = {
            "vacancies_found": index,
            "vacancies_processed": len(salaries),
            "average_salary": get_average_salary(salaries)
        }

    return hhru_salary_statistics


def get_sj_vacancies(client_secret, keyword):

    sj_vacancies_url = "https://api.superjob.ru/2.0/vacancies/"

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

        sj_response = requests.get(
            sj_vacancies_url,
            params=params,
            headers=headers
        )
        sj_response.raise_for_status()
        sj_vacancies = sj_response.json()

        yield from sj_vacancies["objects"]

        if not sj_vacancies["more"]:
            break


def get_sj_vacancy_statistics(programming_languages, client_secret):

    sj_salary_statistics = {}

    for language in programming_languages:

        index = 0
        salaries = []
        vacancies = get_sj_vacancies(client_secret, language)

        for index, vacancy in enumerate(vacancies, start=1):
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                salaries.append(salary)

        sj_salary_statistics[language] = {
            "vacancies_found": index,
            "vacancies_processed": len(salaries),
            "average_salary": get_average_salary(salaries)
        }

    return sj_salary_statistics


def get_average_salary(salaries):
    if not salaries:
        return 0
    return int(sum(salaries)/len(salaries))


def predict_rub_salary_sj(vacancy):
    if not vacancy["currency"] == "rub":
        return

    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]

    if salary_from or salary_to:
        return predict_salary(salary_from, salary_to)


if __name__ == "__main__":
    main()
