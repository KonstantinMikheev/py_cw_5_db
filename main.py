from src.config import config
from src.dbmanager import DBManager
from src.utils import get_employers_from_list, get_vacancies, create_database, save_data_to_database
from src.config import EMPLOYERS_IDS


def main():
    """ Функция взаимодействия с запросами клиента"""
    params = config()
    employers_data = get_employers_from_list(EMPLOYERS_IDS)
    vacancies_data = get_vacancies(EMPLOYERS_IDS)
    create_database('vacancies_hh_ru', params)
    save_data_to_database(employers_data, vacancies_data, 'vacancies_hh_ru', params)
    db_manager = DBManager("vacancies_hh_ru", params)
    print(f'Выберите запрос, либо введите слово "стоп": \n'
          f'1 - Список всех компаний и количество вакансий у каждой компании\n'
          f'2 - Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n'
          f'3 - Средняя зарплата по вакансиям\n'
          f'4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
          f'5 - Список всех вакансий, в названии которых содержится запрашиваемое слово\n')
    user_request = input().strip().lower()
    if user_request == '1':
        print(f"Ответ на Ваш запрос: {db_manager.get_companies_and_vacancies_count()}")
    elif user_request == '2':
        print(f"Ответ на Ваш запрос: {db_manager.get_all_vacancies()}")
    elif user_request == '3':
        print(f"Ответ на Ваш запрос: {db_manager.get_avg_salary()}")
    elif user_request == '4':
        print(f"Ответ на Ваш запрос: {db_manager.get_vacancies_with_higher_salary()}")
    elif user_request == '5':
        user_input = input(f'Введите слово: ')
        print(f"Ответ на Ваш запрос: {db_manager.get_vacancies_with_keyword(user_input)}")
    else:
        print(f"Введён неверный запрос")


if __name__ == "__main__":
    main()
