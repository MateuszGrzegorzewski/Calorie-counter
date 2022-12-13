from main import create_app
from models.food import FoodModel


class TestFood():
    def test_create_food(self):
        food = FoodModel('test', 450)

        assert food is not None
        assert food.foodstuff == 'test'
        assert food.calories == 450
