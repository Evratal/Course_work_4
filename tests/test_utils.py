import pytest
from unittest.mock import MagicMock, patch
from src.utils import user_interaction
from src.jsonvacancystorage import JsonVacancyStorage

@pytest.fixture
def mock_hh_api():
    """Создает фиктивный экземпляр HH API."""
    return MagicMock()

@pytest.fixture
def mock_json_storage(mocker):
    """Создает фиктивный экземпляр JsonVacancyStorage."""
    return mocker.patch('src.jsonvacancystorage.JsonVacancyStorage', autospec=True)

def test_user_interaction_search_vacancies(mock_hh_api, mock_json_storage):
    """Тестирование поиска вакансий по запросу."""
    mock_hh_api.load_vacancies.return_value = [
        {'name': 'Менеджер по продажам', 'salary': {'from': 100000}, 'snippet': {'responsibility': 'Ответственность за продажи'}},
        {'name': 'Менеджер по проектам', 'salary': {'from': 120000}, 'snippet': {'responsibility': 'Управление проектами'}}
    ]

    # Имитация ввода пользователя
    inputs = iter(['1', 'менеджер', '2', '4'])
    with patch('builtins.input', lambda _: next(inputs)):
        user_interaction(mock_hh_api)

    # Проверяем, что метод load_vacancies был вызван с правильным аргументом
    mock_hh_api.load_vacancies.assert_called_once_with('менеджер')

    # Проверяем, что вакансии были добавлены в хранилище
    mock_json_storage.return_value.add_vacancy.assert_any_call({'name': 'Менеджер по продажам', 'salary': {'from': 100000}})
    mock_json_storage.return_value.add_vacancy.assert_any_call({'name': 'Менеджер по проектам', 'salary': {'from': 120000}})

def test_user_interaction_no_vacancies(mock_hh_api, mock_json_storage):
    """Тестирование случая, когда вакансии не найдены."""
    mock_hh_api.load_vacancies.return_value = []

    inputs = iter(['1', 'менеджер', '4'])
    with patch('builtins.input', lambda _: next(inputs)):
        user_interaction(mock_hh_api)

    # Проверяем, что метод load_vacancies был вызван
    mock_hh_api.load_vacancies.assert_called_once_with('менеджер')
    # Проверяем, что add_vacancy не был вызван, так как вакансий нет
    mock_json_storage.return_value.add_vacancy.assert_not_called()

def test_user_interaction_top_n_vacancies(mock_hh_api, mock_json_storage):
    """Тестирование получения топ N вакансий по зарплате."""
    mock_hh_api.load_vacancies.return_value = [
        {'name': 'Менеджер по продажам', 'salary': {'from': 100000}, 'snippet': {'responsibility': 'Ответственность за продажи'}},
        {'name': 'Менеджер по проектам', 'salary': {'from': 120000}, 'snippet': {'responsibility': 'Управление проектами'}}
    ]

    inputs = iter(['2', 'менеджер', '2', '4'])
    with patch('builtins.input', lambda _: next(inputs)):
        user_interaction(mock_hh_api)

    # Проверяем, что метод load_vacancies был вызван
    mock_hh_api.load_vacancies.assert_called_once_with('менеджер')
    # Проверяем, что вакансии были добавлены в хранилище
    assert mock_json_storage.return_value.add_vacancy.call_count == 2  # Должно быть 2 добавленных вакансии

def test_user_interaction_exit(mock_hh_api):
    """Тестирование выхода из программы."""
    inputs = iter(['4'])
    with patch('builtins.input', lambda _: next(inputs)):
        user_interaction(mock_hh_api)

    # Проверяем, что метод load_vacancies не был вызван
    mock_hh_api.load_vacancies.assert_not_called()