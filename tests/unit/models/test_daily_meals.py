from main import create_app
from models.daily_meals import DailyMealsModel, ProductsToDailyMealsModel


class TestDailyMeals():
    def test_create_daily_meals(self):
        meal = DailyMealsModel('2022-12-13', 'breakfast')

        assert meal is not None
        assert meal.date == '2022-12-13'
        assert meal.mealtime == 'breakfast'

    def test_create_product_to_daily_meals(self):
        product = ProductsToDailyMealsModel(
            '2022-12-13', 'breakfast', 2, 250, 1)

        assert product is not None
        assert product.date_of_meal == '2022-12-13'
        assert product.name_of_meal == 'breakfast'
        assert product.product_id == 2
        assert product.weight == 250
        assert product.user_id == 1
