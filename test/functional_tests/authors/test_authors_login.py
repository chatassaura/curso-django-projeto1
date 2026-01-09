import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import \
    expected_conditions as EC  # <--- Adicionado
from selenium.webdriver.support.ui import WebDriverWait  # <--- Adicionado

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user',
            password=string_password
        )

        # Usuário abre a Página de Login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # usuario Vê o Formulario de Login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuário digita o seu usuario e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuário envia o formulário
        form.submit()

        # ESPERA EXPLICÍTA: Aguarda até que o texto de sucesso apareça no
        # corpo da página
        # Isso evita o erro de "NoSuchElementException" durante a recarga da
        #  página
        success_message = f'Your are logged in with {user.username}'
        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'body'),
                success_message
            )
        )

        # Usuário vê a mensagem de Login com sucesso e seu nome
        self.assertIn(
            success_message,
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalida(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )
        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')

        username.send_keys(" ")
        password.send_keys(" ")
        form.submit()

        # Aguarda a mensagem de erro aparecer
        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'body'),
                'Invalid username or password'
            )
        )

        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalida_credential(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )
        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')

        username.send_keys("NaoExiste")
        password.send_keys("Sem@Senh4")
        form.submit()

        # Aguarda a mensagem de erro aparecer
        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'body'),
                'Invalid credentials'
            )
        )

        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
