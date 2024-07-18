from src.config import config
from src.utils import get_employers_from_list, get_vacancies, create_database, save_data_to_database
from src.config import EMPLOYERS_IDS


def main():
    params = config()

    employers_data = get_employers_from_list(EMPLOYERS_IDS)
    vacancies_data = get_vacancies(EMPLOYERS_IDS)

    create_database('vacancies_hh_ru', params)
    save_data_to_database(employers_data, vacancies_data, 'vacancies_hh_ru', params)


if __name__ == "__main__":
    main()
