import pytest
from src.vacancy import Vacancy

class TestVacancy:
    def test_initialization(self):
        vacancy = Vacancy("1", "Vacancy 1", {"from": 50000}, "http://example.com", {"name": "Employer 1"},
                          {"responsibility": "Description"})
        assert vacancy.id == "1"
        assert vacancy.name == "Vacancy 1"
        assert vacancy.salary == {"from": 50000}
        assert vacancy.url == "http://example.com"
        assert vacancy.employer == {"name": "Employer 1"}
        assert vacancy.snippet == {"responsibility": "Description"}

    def test_validate_salary(self):
        vacancy = Vacancy("1", "Vacancy 1", None, "http://example.com", {"name": "Employer 1"},
                          {"responsibility": "Description"})
        assert vacancy.salary == 0  # Проверяем, что зарплата валидируется в 0

        vacancy = Vacancy("2", "Vacancy 2", -1000, "http://example.com", {"name": "Employer 2"},
                          {"responsibility": "Description"})
        assert vacancy.salary == 0  # Проверяем, что отрицательная зарплата валидируется в 0

        vacancy = Vacancy("3", "Vacancy 3", {"from": 60000}, "http://example.com", {"name": "Employer 3"},
                          {"responsibility": "Description"})
        assert vacancy.salary == {"from": 60000}  # Проверяем, что положительная зарплата остается без изменений

    def test_comparison_operators(self):
        vacancy1 = Vacancy("1", "Vacancy 1", {"from": 50000}, "http://example.com", {"name": "Employer 1"},
                           {"responsibility": "Description"})
        vacancy2 = Vacancy("2", "Vacancy 2", {"from": 60000}, "http://example.com", {"name": "Employer 2"},
                           {"responsibility": "Description"})

        assert vacancy1 < vacancy2  # Проверка оператора <
        assert vacancy1 <= vacancy2  # Проверка оператора <=
        assert vacancy2 > vacancy1  # Проверка оператора >
        assert vacancy2 >= vacancy1  # Проверка оператора >=
        assert not (vacancy1 == vacancy2)  # Проверка оператора ==

        vacancy3 = Vacancy("3", "Vacancy 3", {"from": 60000}, "http://example.com", {"name": "Employer 3"},
                           {"responsibility": "Description"})
        assert vacancy2 == vacancy3  # Проверка оператора == для равных зарплат

    def test_str_method(self):
        vacancy = Vacancy("1", "Vacancy 1", {"from": 50000}, "http://example.com", {"name": "Employer 1"},
                          {"responsibility": "Description"})
        expected_str = "Вакансия: Vacancy 1, Зарплата: {'from': 50000}, Ссылка: http://example.com, Описание: {'responsibility': 'Description'}"
        assert str(vacancy) == expected_str