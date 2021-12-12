# Programming vacancies compare

This script calculate the average salary for most popular programming language in Moscow. Jobs are taken from the HeadHunter and SuperJob sites.


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).


## Usage
0. Create environment variables. See a topic "SuperJob API" for example.
1. Run `main.py` to display salary statistics.
```
python main.py
```
![](https://github.com/vip-v2a/language-salary/blob/8793aee628bc2e6772a647bed1622018954501db/ext/example.gif)


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


## HeadHunter API

[Developers page](https://dev.hh.ru/).
[API general information](https://github.com/hhru/api/blob/master/docs/general.md).
[How to get vacancies information](https://github.com/hhru/api/blob/master/docs/vacancies.md).

### Vacancy parameters
- [Specializations](https://api.hh.ru/specializations).
- [Professional roles](https://api.hh.ru/professional_roles).
- [Areas](https://api.hh.ru/areas).


## SuperJob API

[API description](https://api.superjob.ru/).

To use all API methods, you need [to register your application](https://api.superjob.ru/register). After registration, you get access parameters: "ID", "Secret key". You need to set these parameters in environment variables `SUPERJOB_ID`, `SUPERJOB_API_KEY`. To do this, type commands at the Command Prompt:

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
- [Catalogues](https://api.superjob.ru/2.0/catalogues/).
- [Town](https://api.superjob.ru/2.0/towns/).