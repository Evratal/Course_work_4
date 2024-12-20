
from src.parser import Parser
import requests

from src.jsonvacancystorage import JsonVacancyStorage


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    """
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []

    def connect(self):
        """Подключение к API."""
        # Проверка доступности API
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            print("Подключение к API успешно!")
        else:
            raise Exception(f"Ошибка подключения к API: {response.status_code}")


    def load_vacancies(self, keyword:str):
        """Загружаем вакансии по заданному ключевому слову"""
        self.params['text'] = keyword
        self.params['page'] = 0  # Сброс страницы перед загрузкой
        self.vacancies = []  # Инициализируем список вакансий

        while self.params.get('page') < 20: # Ограничиваем до 20 страниц
            response = requests.get(self.url, headers=self.headers, params=self.params)

            if response.status_code == 200:
                data = response.json()
                vacancies = data.get('items', [])

                if not vacancies: #Если вакансий нет, выходим из цикла
                   break

                self.vacancies.extend(vacancies)     # Добавляем новые вакансии
                self.params['page'] += 1        # Переходим на следующую страницу

            else:
                print(f"Ошибка получения вакансий: {response.status_code}")
                break  # Выходим из цикла при ошибке

        return self.vacancies  # Возвращаем список вакансий

