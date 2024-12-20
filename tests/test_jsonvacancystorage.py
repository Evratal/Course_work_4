import pytest
import os
import json
from src.jsonvacancystorage import JsonVacancyStorage  # Убедитесь, что импорт правильный


@pytest.fixture
def json_storage(tmp_path):
    """Создает временный файл для тестирования."""
    file_path = tmp_path / "test_vacancies.json"
    storage = JsonVacancyStorage(file_path)
    return storage, file_path


def test_add_vacancy(json_storage):
    storage, file_path = json_storage
    vacancy = {
        'name': 'Менеджер по продажам',
        'salary': {'from': 100000}
    }

    storage.add_vacancy(vacancy)

    # Проверяем, что вакансия добавилась в файл
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]['name'] == 'Менеджер по продажам'


def test_get_vacancies(json_storage):
    storage, file_path = json_storage
    vacancy1 = {
        'name': 'Менеджер по продажам',
        'salary': {'from': 100000}
    }
    vacancy2 = {
        'name': 'Менеджер по проектам',
        'salary': {'from': 120000}
    }
    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)

    # Получаем вакансии по критериям
    results = storage.get_vacancies(name='Менеджер по продажам')
    assert len(results) == 1
    assert results[0]['name'] == 'Менеджер по продажам'


def test_delete_vacancy(json_storage):
    storage, file_path = json_storage
    vacancy1 = {
        'name': 'Менеджер по продажам',
        'salary': {'from': 100000}
    }
    vacancy2 = {
        'name': 'Менеджер по проектам',
        'salary': {'from': 120000}
    }
    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)

    # Удаляем вакансию
    storage.delete_vacancy(vacancy1['name'])

    # Проверяем, что вакансия была удалена
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]['name'] == 'Менеджер по проектам'


def test_initialization_creates_empty_file(json_storage):
    storage, file_path = json_storage
    # Проверяем, что файл инициализирован как пустой
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert data == []  # Должен быть пустой список