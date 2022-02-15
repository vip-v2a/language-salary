import os
import logging
import requests
from itertools import count
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_hhru_vacancies(text):

    url = "https://api.hh.ru/vacancies"
    moscow_id = "1"
    past_days_period = 30
    programming_id = "96"
    search_field = "name"

    params = {
        "professional_role": programming_id,
        "area": moscow_id,
        "period": past_days_period,
        "search_field": search_field,
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

        salaries, vacancies_found = process_hhru_vacancies(language)

        statistics[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(salaries),
            "average_salary": get_average_salary(salaries)
        }

    return statistics


def process_hhru_vacancies(language):
    salaries = []

    for vacancies_found, vacancies in get_hhru_vacancies(language):
        for vacancy in vacancies:
            salary = predict_rub_salary_hh(vacancy)
            if salary:
                salaries.append(salary)
    return salaries, vacancies_found


def get_sj_vacancies(client_secret, keyword):

    url = "https://api.superjob.ru/2.0/vacancies/"
    moscow_id = 4
    programming_id = 48
    results_per_page = 100

    headers = {
        "X-Api-App-Id": client_secret
    }

    params = {
        "town": moscow_id,
        "catalogues": programming_id,
        "keyword": keyword,
        "count": results_per_page
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

        yield vacancies["total"], vacancies["objects"]

        if not vacancies["more"]:
            break


def get_sj_vacancy_statistics(programming_languages, client_secret):

    statistics = {}

    for language in programming_languages:

        salaries, vacancies_found = process_sj_vacancies(client_secret,
                                                         language)

        statistics[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(salaries),
            "average_salary": get_average_salary(salaries)
        }

    return statistics


def process_sj_vacancies(client_secret, language):
    salaries = []

    for vacancies_found, vacancies in get_sj_vacancies(client_secret,
                                                       language):
        for vacancy in vacancies:
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                salaries.append(salary)
    return salaries, vacancies_found


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
