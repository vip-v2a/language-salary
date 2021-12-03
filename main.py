import time
import requests


def get_hhru_response(text, area_id="1", period=30,
                      professional_role_id="96"):
    hhru_url = "https://api.hh.ru/vacancies"
    params = {
        "professional_role": professional_role_id,
        "area": area_id,
        "period": period,
        "text": text
    }

    hhru_response = requests.get(hhru_url, params=params)
    hhru_response.raise_for_status()

    return hhru_response.json()


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
    language_salary = {}

    for language in programming_languages[:1]:
        hhru_response = get_hhru_response(language)
        founded_vacancies = hhru_response["found"]
        vacancies = hhru_response["items"]
        for vacancy in vacancies:
            salary = predict_rub_salary(vacancy)
            print(salary)
        # time.sleep(1)

    print(language_salary)


if __name__ == '__main__':
    main()
