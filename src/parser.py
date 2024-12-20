from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def connect(self):
        """Подключение к API."""
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str):
        """Получение вакансий по ключевому слову."""
        pass

