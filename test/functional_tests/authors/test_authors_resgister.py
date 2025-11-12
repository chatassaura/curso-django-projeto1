import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.fill_form_dummy_data(form)

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            form.find_element(By.NAME, 'email').send_keys('teste@teste.com')
            first_name_input = self.get_by_placeholder(form, 'Ex.: John')
            first_name_input.send_keys(" ")
            first_name_input.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your first name', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            form.find_element(By.NAME, 'email').send_keys('teste@teste.com')
            last_name_input = self.get_by_placeholder(form, 'Ex.: Doe')
            last_name_input.send_keys(" ")
            last_name_input.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your last name', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            form.find_element(By.NAME, 'email').send_keys('teste@teste.com')
            username_input = self.get_by_placeholder(form, 'Ex.: Doe')
            username_input.send_keys(" ")
            username_input.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field must not be empty', form.text)

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            form.find_element(By.NAME, 'email').send_keys('teste@teste')
            email_input = self.get_by_placeholder(form, 'Ex.: Doe')
            email_input.send_keys(" ")
            email_input.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The e-mail must be valid.', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            form.find_element(By.NAME, 'email').send_keys('teste@teste.com')
            password1 = self.get_by_placeholder(form, 'Type your password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password1.send_keys("P@ssw0rd")
            password2.send_keys("P@ssw0rd_Different")
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Password and password2 must be equal', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.get_by_placeholder(form, 'Ex.: John').send_keys('John')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Doe')
        self.get_by_placeholder(form, 'Your username').send_keys('johndoe')
        self.get_by_placeholder(
            form, 'Your e-mail'
                                ).send_keys('johndoe@gmail.com')
        self.get_by_placeholder(
            form, 'Type your password'
            ).send_keys('P@ssw0rd1')
        self.get_by_placeholder(
            form, 'Repeat your password'
            ).send_keys('P@ssw0rd1')

        form.submit()

        self.assertIn(
            'Your user is created, please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
