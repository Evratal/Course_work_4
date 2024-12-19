import json
import os

from src.vacancystorage import VacancyStorage


class JsonVacancyStorage(VacancyStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        # Убедимся, что файл существует, если нет, создадим пустой файл
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump([], file)  # Создаем пустой массив JSON

    def add_vacancy(self, vacancy):
        """Добавление вакансии в файл."""
        with open(self.file_path, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data.append(vacancy.__dict__)  # Добавляем словарь вакансии
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_vacancies(self, **criteria):
        """Получение данных из файла по указанным критериям."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Фильтрация по критериям
            filtered_data = []

            for vacancy in data:
                matches_all_criteria = True  # Предполагаем, что вакансия соответствует всем критериям

                for key, value in criteria.items():
                    if vacancy.get(key) != value:
                        matches_all_criteria = False  # Если хотя бы одно условие не выполнено
                        break  # Прекращаем проверку, так как уже знаем, что не соответствует

                if matches_all_criteria:
                    filtered_data.append(vacancy)  # Добавляем вакансию в список, если она соответствует всем критериям
            return filtered_data

    def delete_vacancy(self, vacancy_id):
        """Удаление информации о вакансии."""
        with open(self.file_path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data = [vacancy for vacancy in data if vacancy.get('id') != vacancy_id]  # Предполагаем, что у вакансии есть поле 'id'
            f.seek(0)
            f.truncate()  # Очищаем файл
            json.dump(data, f, ensure_ascii=False, indent=4)