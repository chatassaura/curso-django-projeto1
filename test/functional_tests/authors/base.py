# noqa: E501
import time
from unittest.mock import patch

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )

    def sleep(self, seconds=5):
        time.sleep(seconds)

    # 1. Testar se o valor padrão (5 segundos) é usado
    # O patch substitui a função time.sleep do módulo 'time' global
    @patch('time.sleep')
    def test_sleep_uses_default_five_seconds_if_no_argument_is_given(self, mock_time_sleep):
        # Arrange
        base_test = AuthorsBaseTest()

        # Act
        base_test.sleep() # Chama sem argumentos

        # Assert
        # Verifica se time.sleep foi chamado com 5 (o valor padrão)
        mock_time_sleep.assert_called_once_with(5)

    # 2. Testar se um valor customizado é usado
    @patch('time.sleep')
    def test_sleep_uses_correct_custom_seconds(self, mock_time_sleep):
        # Arrange
        custom_seconds = 10
        base_test = AuthorsBaseTest()
        # Act
        base_test.sleep(seconds=custom_seconds)
        # Assert
        # Verifica se time.sleep foi chamado com o valor customizado
        mock_time_sleep.assert_called_once_with(custom_seconds)

    # 3. Testar se a função não foi chamada quando não deveria
    # (Exemplo Negativo)
    @patch('time.sleep')
    def test_sleep_is_not_called_outside_of_method_execution(self, mock_time_sleep):
        # Arrange
        # base_test = AuthorsBaseTest()
        # Act/Assert: Nenhuma chamada a base_test.sleep() é feita
        # Assert
        # Verifica se time.sleep não foi chamado
        mock_time_sleep.assert_not_called()
