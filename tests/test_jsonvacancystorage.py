import pytest
import json
import os
from unittest.mock import MagicMock, patch
from src.vacancystorage import VacancyStorage
from src.jsonvacancystorage import JsonVacancyStorage

@pytest.fixture
def json_storage(tmp_path):
    # Создаем временный файл для тестов
    file_path = tmp_path / "vacancies.json"
    storage = JsonVacancyStorage(file_path)
    return storage, file_path

def test_add_vacancy(json_storage):
    storage, file_path = json_storage
    class MockVacancy:
        def __init__(self, name, salary):
            self.name = name
            self.salary = salary

    vacancy = MockVacancy("Vacancy 1", {"from": 50000})

    storage.add_vacancy(vacancy)

    # Проверяем, что файл содержит добавленную вакансию
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]['name'] == "Vacancy 1"
        assert data[0]['salary'] == {"from": 50000}

def test_get_vacancies(json_storage):
    storage, file_path = json_storage
    class MockVacancy:
        def __init__(self, name, salary):
            self.name = name
            self.salary = salary

    # Добавляем несколько вакансий
    storage.add_vacancy(MockVacancy("Vacancy 1", {"from": 50000}))
    storage.add_vacancy(MockVacancy("Vacancy 2", {"from": 60000}))
    storage.add_vacancy(MockVacancy("Vacancy 3", {"from": 70000}))

    # Фильтруем по критерию
    vacancies = storage.get_vacancies(name="Vacancy 2")
    assert len(vacancies) == 1
    assert vacancies[0]['name'] == "Vacancy 2"

    # Проверка на отсутствие вакансий
    vacancies = storage.get_vacancies(name="Vacancy 4")
    assert len(vacancies) == 0

def test_delete_vacancy(json_storage):
    storage, file_path = json_storage

    class MockVacancy:
        def __init__(self, id, name, salary):
            self.id = id
            self.name = name
            self.salary = salary

    # Добавляем несколько вакансий с id
    storage.add_vacancy(MockVacancy(1, "Vacancy 1", {"from": 50000}))
    storage.add_vacancy(MockVacancy(2, "Vacancy 2", {"from": 60000}))

    # Удаляем вакансию с id 2
    storage.delete_vacancy(2)

    # Проверяем, что вакансия была удалена
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert len(data) == 1  # Ожидаем, что осталась только одна вакансия
        assert data[0]['name'] == "Vacancy 1"  # Ожидаем, что осталась именно эта вакансия