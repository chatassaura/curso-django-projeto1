from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')
    
    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_view_loads_no_recipe_fouds_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(' <h1>Nenhuma receita encontrada. 😢</h1>', response.content.decode('utf-8'))
    
    def test_recipe_categoty_url_is_correct(self):
        category_url = reverse('recipes:category', kwargs={'category_id':1})
        self.assertEqual(category_url, '/' \
        'recipes/category/1')

    def test_recipe_categoty_view_return_404_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_recipe_url_is_correct(self):
        recipe_url = reverse('recipes:recipe', args=(1,))
        self.assertEqual(recipe_url, '/recipes/1')

    def test_recipe_detail_view_return_404_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        self.assertEqual(response.status_code, 404)
