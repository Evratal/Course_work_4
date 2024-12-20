import pytest
import requests
from unittest.mock import patch, Mock
from src.hh import HH



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

