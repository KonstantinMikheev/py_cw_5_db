import json
from typing import Any

import psycopg2
import requests


def get_employers_from_list(employers_ids: list[str]) -> list[dict]:
    """Функция подключения к API HH.RU и получения информации о работодателях"""
    employers_data = []
    for employer_id in employers_ids:
        url = f'https://api.hh.ru/employers/{employer_id}'
        response = requests.get(url)
        if response.status_code == 200:
            employer = response.json()
            employers_data.append(employer)
        else:
            print(f'''Ошибка запроса данных. Статус запроса: {response.status_code},
                response: {response.text}''')
    return employers_data


def get_vacancies(employers_ids: list[str]) -> list[dict]:
    """Функция подключения к API HH.RU и получения вакансий по id работодателей"""
    vacancies_data = []
    for employer_id in employers_ids:
        url = f'https://api.hh.ru/vacancies?employer_id={employer_id}'
        params = {
            'page': 0,
            'per_page': 100,
            'only_with_salary': True
        }
        response = requests.get(url)
        if response.status_code == 200:
            while params.get('page') != 5:
                response_with_params = requests.get(url, params=params)
                vacancies_data.extend(response_with_params.json().get('items'))
                params['page'] += 1
        else:
            print(f'''Ошибка запроса данных. Статус запроса: {response.status_code}, 
                response: {response.text}''')
    return vacancies_data


def create_database(database_name: str, params: dict):
    """Функция создания базы данных"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name};')
    cur.execute(f'CREATE DATABASE {database_name};')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                employer_name VARCHAR(200) NOT NULL,
                city VARCHAR(50),
                url VARCHAR(300),
                vacancies_url VARCHAR(350),
                open_vacancies SMALLINT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id),
                employer_name VARCHAR(200) NOT NULL,
                vacancy_name VARCHAR NOT NULL,
                requirement TEXT,
                responsibility TEXT,
                city VARCHAR(50),
                salary BIGINT NOT NULL,
                currency VARCHAR(50),
                published_at DATE,
                vacancy_url TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(
        employers_data: list[dict[str, Any]],
        vacancies_data: list[dict[str, Any]],
        database_name: str,
        params: dict
) -> None:
    """
    Функция добавления информации в базу данных
    :param employers_data: информация о работодателе
    :param vacancies_data: информация о вакансиях
    :param database_name: название базы данных
    :param params: параметры подключения
    """

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in employers_data:
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name, city, url, vacancies_url,
                open_vacancies)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (employer['id'], employer['name'],
                 employer['area']['name'], employer['site_url'], employer['vacancies_url'], employer['open_vacancies'])
            )

        for vacancy in vacancies_data:
            salary_from = vacancy['salary'].get('from') if vacancy['salary'].get('from') is not None else 0
            salary_to = vacancy['salary'].get('to') if vacancy['salary'].get('to') is not None else 0
            if salary_from <= salary_to:
                salary = salary_to
            else:
                salary = salary_from

            currency = vacancy['salary'].get('currency') if vacancy['salary'] else None
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, employer_id, employer_name, vacancy_name, requirement,
                responsibility, city, salary, currency, published_at, vacancy_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (vacancy['id'], vacancy['employer']['id'], vacancy['employer']['name'], vacancy['name'],
                 vacancy['snippet']['requirement'], vacancy['snippet']['responsibility'], vacancy['area'].get('name'),
                 salary, currency, vacancy['published_at'], vacancy['alternate_url'])
            )

    conn.commit()
    conn.close()


# def save_json(data):
#     with open('/home/kmikheev/snap/python/PycharmProjects/py_cw_5_db/data.json', "w", encoding='utf-8') as file:
#         json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    a = get_vacancies(['955', '575665'])
    save_json(a)

