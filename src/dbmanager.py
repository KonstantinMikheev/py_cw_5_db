import psycopg2

from src.config import config


class DBManager:
    """"""
    db_name: str  # Database title
    params: dict  # Parameters for connection to DB via PostgreSQL

    __slots__ = ['db_name', 'params', 'conn', 'cur']

    def __init__(self, db_name, params) -> None:
        self.db_name = db_name
        self.conn = psycopg2.connect(dbname=db_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """"""
        self.cur.execute('''
            SELECT employer_name, COUNT(*) FROM vacancies
            GROUP BY employer_name;
            ''')
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute('''
            SELECT vacancy_name, employer_name, salary, vacancy_url FROM vacancies
            ORDER BY employer_name;
            ''')
        return self.cur.fetchall()

    def get_avg_salary(self):
        """SELECT vacancy_name, ROUND(AVG(salary)::numeric, 2) as average_salary FROM vacancies
        GROUP BY vacancy_name;"""
        self.cur.execute('''
            SELECT ROUND(AVG(salary)::numeric, 2) AS average_salary FROM vacancies;
            ''')
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """"""
        self.cur.execute('''
            SELECT * FROM vacancies
            WHERE salary > (SELECT ROUND(AVG(salary)::numeric, 2) as average_salary FROM vacancies);
            ''')
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """"""
        self.cur.execute(f'''
            SELECT * FROM vacancies 
            WHERE vacancy_name LIKE '%{keyword}%';
                    ''')
        return self.cur.fetchall()

    def __del__(self):
        self.cur.close()


if __name__ == '__main__':
    params = config()
