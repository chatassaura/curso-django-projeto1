from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
        # Usuario abre a pagina
        title_needed = 'this is what I need'

        recipes[0].title = title_needed
        recipes[0].save()

        self.browser.get(self.live_server_url)

        # ve um campo de buca com o texto "search for a recipe..."
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for recipes..."]'
        )

        # clina nesse input e digita o termo de busca
        # "Recipe Title 1" para encontrar a receita com esse titulo
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
           title_needed,
           self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

        self.sleep(6)
