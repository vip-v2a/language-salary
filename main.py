import logging
import os
import requests
from itertools import count
from dotenv import load_dotenv


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

    load_dotenv()
    sj_login = os.getenv("SUPERJOB_LOGIN")
    sj_password = os.getenv("SUPERJOB_PASSWORD")
    sj_id = os.getenv("SUPERJOB_ID")
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
    sj_salary_statistics = get_sj_vacancy_statistics(
        programming_languages,
        sj_id,
        sj_api_key,
        sj_login,
        sj_password
    )
    print(sj_salary_statistics)


def get_hhru_vacancy_statistics(programming_languages):

    hhru_salary_statistics = {}

    for language in programming_languages:

        salaries = []
        vacancies = get_hhru_vacancies(language)

        for vacancy in vacancies:
            salary = predict_rub_salary_hh(vacancy)
            if salary:
                salaries.append(salary)

        hhru_salary_statistics[language] = {
            "vacancies_found": len(vacancies),
            "vacancies_processed": len(salaries),
            "average_salary": get_average_salary(salaries)
        }

    return hhru_salary_statistics


def is_ok_sj_authorization(login, password, client_id, client_secret):

    oauth2_url = "https://api.superjob.ru/2.0/oauth2/password/"
    params = {
        "login": login,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret
    }

    oauth2_response = requests.get(oauth2_url, params)
    oauth2_response.raise_for_status()

    return oauth2_response.ok


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



def get_sj_vacancy_statistics(programming_languages, client_id,
                              client_secret, login, password):

    sj_salary_statistics = {}

    if not is_ok_sj_authorization(login, password, client_id, client_secret):
        logging.warning(
            "Failed authorization on the SuperJob website."
        )
        return

    for language in programming_languages:

        index = 0
        salaries = []
        vacancies = get_sj_vacancies(client_secret, language)
        print(language)

        for index, vacancy in enumerate(vacancies, start=1):
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                salaries.append(salary)

        print(salaries)
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
