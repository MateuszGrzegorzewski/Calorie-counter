from main import create_app
from models.meals_fav import MealModel, ProductsToMealsModel


class TestDailyMeals():
    def test_create_meals(self):
        meal = MealModel(name='test', user_id=1)

        assert meal is not None
        assert meal.name == 'test'
        assert meal.user_id == 1

    def test_create_product_to_daily_meals(self):
        product = ProductsToMealsModel(1, 2, 250)

        assert product is not None
        assert product.favmeal_id == 1
        assert product.product_id == 2
        assert product.weight == 250
