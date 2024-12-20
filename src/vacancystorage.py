from abc import ABC, abstractmethod

class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавление вакансии в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, **criteria):
        """Получение данных из файла по указанным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        """Удаление информации о вакансии."""
        pass