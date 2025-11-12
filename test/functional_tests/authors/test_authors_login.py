import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

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

        # Usuário vê a mensagem de Login com sucesso e seu nome
        self.assertIn(
            f'Your are logged in with {user.username}',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        # end Test

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalida(self):
        # Usuário abre a página de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # usuario ve o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, "main-form")

        # E tenta enviar valores vazios
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(" ")
        password.send_keys(" ")

        # Envia Formulario
        form.submit()

        # Vê uma mensagem de erro
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalida_credential(self):
        # Usuário abre a página de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # usuario ve o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, "main-form")

        # E tenta enviar valores vazios
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys("NaoExiste")
        password.send_keys("Sem@Senh4")

        # Envia Formulario
        form.submit()

        # Vê uma mensagem de erro
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
