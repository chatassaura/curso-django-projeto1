from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base import RecipeBaseFunctionalTest


# from django.test import LiveServerTestCase
@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('No recipes found here 😢', body)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)

        # Find the search input element
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # Type the search term and submit
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        # --- NOVO PONTO DE ESPERA MAIS ESTÁVEL ---
        # Espera até que o texto da receita (recipes[0].title) esteja presente
        # no BODY da nova página de busca. O By.TAG_NAME, 'body' garante que a
        # referência não será Stale.
        WebDriverWait(self.browser, 5).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'body'),
                recipes[0].title
            )
        )

        # --- RELOCALIZAR E ASSERTAR ---
        # Agora que sabemos que o texto existe, re-localize o container
        # e faça a asserção.
        main_content_list = self.browser.find_element(
            By.CLASS_NAME,
            'main-content-list'
        )

        # Assert that the recipe title is present in the list's text
        self.assertIn(
            recipes[0].title,
            main_content_list.text,
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()
        # usuario abre a pagina
        self.browser.get(self.live_server_url)
        # ve que tem uma paginacao e clica na 2
        page2 = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Go to page 2"]'
        )

        page2.click()
        self.sleep()  # espera a pagina carregar
