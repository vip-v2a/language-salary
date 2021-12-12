# Programming vacancies compare

This script calculate the average salary for most popular programming language in Moscow. Jobs are taken from the HeadHunter and SuperJob sites.


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).


## HeadHunter API

[Developers page](https://dev.hh.ru/)
[API general information](https://github.com/hhru/api/blob/master/docs/general.md)
[How to get vacancies information](https://github.com/hhru/api/blob/master/docs/vacancies.md)

### Vacancy parameters
- [Specializations](https://api.hh.ru/specializations)
- [Professional roles](https://api.hh.ru/professional_roles)
- [Areas](https://api.hh.ru/areas)


## SuperJob API

[API description](https://api.superjob.ru/)

To use all API methods, you need [to register your application](https://api.superjob.ru/register). After registration you get access parameters: "ID", "Secret key". You need to set these parameters in environment variables `SUPERJOB_ID`, `SUPERJOB_API_KEY`. To do this, type commands at the Command Prompt:

```
set SUPERJOB_ID=ID
set SUPERJOB_API_KEY=Secret_key
```

To get access token you also need to set your login(`SUPERJOB_LOGIN`) and password(`SUPERJOB_PASSWORD`) from SuperJob site in environment variables:

```
set SUPERJOB_LOGIN=your@email.com
set SUPERJOB_PASSWORD=your_password
```

P.S.: Usually, SuperJob sends the password to the mail after registration.

### Vacancy parameters
- [Catalogues](https://api.superjob.ru/2.0/catalogues/)
- []()
- [Town](https://api.superjob.ru/2.0/towns/)

### Пагинация

К любому запросу, подразумевающему выдачу списка объектов, можно в параметрах
указать `page=N&per_page=M`. Нумерация идёт с нуля, по умолчанию выдаётся
первая (нулевая) страница с 20 объектами на странице. Во всех ответах, где
доступна пагинация, единообразный корневой объект:

```json
{
  "found": 1,
  "per_page": 1,
  "pages": 1,
  "page": 0,
  "items": [{}]
}
```

## Usage
0. Create enviroment variables. See a topic "Create enviroment variable" for example.
1. Run `` to.
```
python download_images.py
```
![]()

2. Run `` to .
```
python space_bot.py
```
Then you see messages in Telegram group:
![]()

## Getting Started
### Prerequisites

You need create environment variables:
- `SUPERJOB_LOGIN` your login from SuperJob site.
- `SUPERJOB_PASSWORD` your password from SuperJob site. It will come to your mail.
- `SUPERJOB_ID` your app ID. You'll get it after registration. It is your access parameters.
- `SUPERJOB_API_KEY` your app Secret key. You'll get it after registration. It is your access parameters.


If you need [creation of virtual environment](https://vc.ru/dev/240211-nastroyka-rabochego-okruzheniya-na-windows-dlya-raboty-s-python).

You need install `requirements.txt`:
```    
pip install -r requirements.txt
```