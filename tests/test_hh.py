import pytest
import requests
from unittest.mock import patch, Mock
from src.hh import HH
from src.savejson import SaveJson


class TestHH:
    @patch('requests.get')
    def test_connect_success(self, mock_get):
        # Настраиваем имитацию успешного ответа
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = HH()
        api.connect()  # Вызов метода connect

        # Проверяем, что метод requests.get был вызван с правильными параметрами
        mock_get.assert_called_once_with(api.url, headers=api.headers)

    @patch('requests.get')
    def test_connect_failure(self, mock_get):
        # Настраиваем имитацию ответа с ошибкой
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        api = HH()
        with pytest.raises(Exception) as excinfo:
            api.connect()

        assert str(excinfo.value) == "Ошибка подключения к API: 404"

    @patch('requests.get')
    def test_load_vacancies_no_items(self, mock_get):
        # Настраиваем имитацию ответа с пустым списком вакансий
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response

        api = HH()
        vacancies = api.load_vacancies("developer")  # Вызов метода, который тестируем

        assert len(vacancies) == 0  # Проверяем, что возвращено 0 вакансий

    @patch('requests.get')
    def test_load_vacancies_error(self, mock_get):
        # Настраиваем имитацию ответа с ошибкой
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        api = HH()
        vacancies = api.load_vacancies("developer")  # Вызов метода, который тестируем

        assert len(vacancies) == 0  # Проверяем, что возвращено 0 вакансий


    @patch('builtins.input', side_effect=['1', 'developer'])  # Имитация ввода пользователя
    @patch('src.hh.HH.load_vacancies')  # Имитация метода load_vacancies
    @patch('builtins.print')  # Имитация функции print
    @patch.object(SaveJson, 'save_file')  # Имитация метода save_file
    def test_user_interaction_success(self, mock_save_file, mock_print, mock_load_vacancies, mock_input):
        # Настраиваем имитацию возвращаемых вакансий
        mock_load_vacancies.return_value = [
            {'name': 'Vacancy 1', 'salary': {'from': 50000}},
            {'name': 'Vacancy 2', 'salary': {'from': 60000}}
        ]
        api = HH()
        api.user_interaction()  # Вызов метода

        # Проверяем, что print был вызван с правильными аргументами
        mock_print.assert_any_call("Найдено 2 вакансий по запросу 'developer':")
        mock_print.assert_any_call("- Vacancy 1 (Зарплата: 50000)")
        mock_print.assert_any_call("- Vacancy 2 (Зарплата: 60000)")

        # Проверяем, что метод save_file был вызван
        mock_save_file.assert_called_once()

    @patch('builtins.input', side_effect=['1', 'developer'])  # Имитация ввода пользователя
    def test_user_interaction_no_vacancies(self, mock_print, mock_load_vacancies, mock_input):
        # Настраиваем имитацию пустого списка вакансий
        mock_load_vacancies.return_value = []
        api = HH()
        api.user_interaction()  # Вызов метода

        # Проверяем, что print был вызван с сообщением об отсутствии вакансий
        mock_print.assert_called_once_with("Вакансии не найдены.")

    @patch('builtins.input', side_effect=['4'])  # Имитация ввода пользователя для выхода
    def test_user_interaction_exit(self, mock_print, mock_input):
        api = HH()
        with patch('builtins.print') as mock_print:
            api.user_interaction()  # Вызов метода
            # Проверяем, что выводится меню команд
            mock_print.assert_any_call("\nДоступные команды:")
            mock_print.assert_any_call("4. Выход")

    # Тест для получения топ N вакансий по зарплате
    @patch('builtins.input', side_effect=['2', 'developer', '2'])  # Имитация ввода
    @patch.object(SaveJson, 'save_file')  # Имитация метода save_file
    def test_user_interaction_top_n_vacancies(self, mock_save_file, mock_print, mock_load_vacancies, mock_input):
        # Настраиваем имитацию возвращаемых вакансий
        mock_load_vacancies.return_value = [
            {'name': 'Vacancy 1', 'salary': {'from': 50000}},
            {'name': 'Vacancy 2', 'salary': {'from': 60000}},
            {'name': 'Vacancy 3', 'salary': {'from': 55000}},
            {'name': 'Vacancy 4', 'salary': None},  # Вакансия без зарплаты
        ]

        api = HH()
        api.user_interaction()  # Вызов метода

        # Проверяем, что print был вызван с правильными аргументами
        mock_print.assert_any_call("Топ 2 вакансий по зарплате для запроса 'developer':")
        mock_print.assert_any_call("- Vacancy 2 (Зарплата: 60000)")
        mock_print.assert_any_call("- Vacancy 3 (Зарплата: 55000)")

        # Проверяем, что метод save_file был вызван
        mock_save_file.assert_called_once()

    # Тест для случая, когда вакансий не найдено
    @patch('builtins.input', side_effect=['2', 'developer', '2'])  # Имитация ввода
    def test_user_interaction_no_vacancies_top_n(self, mock_print, mock_load_vacancies, mock_input):
        # Настраиваем имитацию пустого списка вакансий
        mock_load_vacancies.return_value = []

        api = HH()
        api.user_interaction()  # Вызов метода

        # Проверяем, что print был вызван с сообщением об отсутствии вакансий
        mock_print.assert_called_once_with("Вакансии не найдены.")

    # Тест для поиска вакансий по ключевому слову в описании
    @patch('builtins.input', side_effect=['3', 'ответственность'])  # Имитация ввода

    def test_user_interaction_keyword_search(self, mock_save_file, mock_print, mock_load_vacancies, mock_input):
        # Настраиваем имитацию возвращаемых вакансий
        mock_load_vacancies.return_value = [
            {'name': 'Vacancy 1', 'salary': {'from': 50000},
             'snippet': {'responsibility': 'Основные обязанности: ответственность за проект.'}},
            {'name': 'Vacancy 2', 'salary': {'from': 60000}, 'snippet': {'responsibility': 'Работа с документацией.'}},
            {'name': 'Vacancy 3', 'salary': {'from': 55000}, 'snippet': {'responsibility': None}},
            {'name': 'Vacancy 4', 'salary': None, 'snippet': {}}
        ]

        api = HH()
        api.user_interaction()  # Вызов метода

        # Проверяем, что print был вызван с правильными аргументами
        mock_print.assert_any_call("Вакансии с ключевым словом 'ответственность' в описании:")
        mock_print.assert_any_call("- Vacancy 1 (Зарплата: 50000)")
        mock_print.assert_any_call("- Vacancy 2 (Зарплата: 60000)")

        # Проверяем, что метод save_file был вызван
        mock_save_file.assert_called_once()

    # Тест для случая, когда вакансий не найдено
    @patch('builtins.input', side_effect=['3', 'неизвестное_слово'])  # Имитация ввода
    def test_user_interaction_no_vacancies_keyword_search(self, mock_print, mock_load_vacancies, mock_input):
        # Настраиваем имитацию пустого списка вакансий
        mock_load_vacancies.return_value = []

        api = HH()
        api.user_interaction()  # Вызов метода

        # Проверяем, что print был вызван с сообщением об отсутствии вакансий
        mock_print.assert_called_once_with("Вакансии не найдены.")