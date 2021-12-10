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

    load_dotenv()
    sj_login = os.getenv("SUPERJOB_LOGIN")
    sj_password = os.getenv("SUPERJOB_PASSWORD")
    sj_id = os.getenv("SUPERJOB_ID")
    sj_api_key = os.getenv("SUPERJOB_API_KEY")

    programming_languages = [
        # "Python",
        # "Java",
        # "PHP",
        # "JavaScript",
        # "C++",
        # "Swift",
        # "Ruby",
        # "Go",
        # "React",
        # "C#"
    ]
    hhru_salary_statistics = {}

    for language in programming_languages[:2]:

        salaries = []

        for index, vacancy in enumerate(get_hhru_vacancies(language),
                                        start=1):
            salary = predict_rub_salary(vacancy)
            if salary:
                salaries.append(salary)
            print(language, index)

        hhru_salary_statistics[language] = {
            "vacancies_found": index,
            "vacancies_processed": len(salaries),
            "average_salary": int(sum(salaries)/len(salaries))
        }

    # print(hhru_salary_statistics)
    # sj_access_token = get_sj_access_token(
    #     sj_login,
    #     sj_password,
    #     sj_id,
    #     sj_api_key
    # )
    get_sj_vacancies(sj_api_key, "python")


def get_sj_access_token(login, password, client_id, client_secret):

    oauth2_url = "https://api.superjob.ru/2.0/oauth2/password/"
    params = {
        "login": login,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret
    }

    oauth2_response = requests.get(oauth2_url, params)
    oauth2_response.raise_for_status()

    return oauth2_response.json()["access_token"]


def get_sj_vacancies(client_secret, keyword):

    sj_vacancies_url = "https://api.superjob.ru/2.0/vacancies/"

    headers = {
        "X-Api-App-Id": client_secret
    }

    params = {
        "town": 4,
        "catalogues": 48,
        "keyword": keyword
    }

    sj_response = requests.get(
        sj_vacancies_url,
        params=params,
        headers=headers
    )
    sj_response.raise_for_status()
    sj_vacancies = sj_response.json()["objects"]
    for vacancy in sj_vacancies:
        print(vacancy["profession"], vacancy["town"]["title"])


if __name__ == "__main__":
    main()
