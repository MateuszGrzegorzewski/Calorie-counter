from models.meals_fav import MealModel, ProductsToMealsModel
from models.food import FoodModel
from flask_restful import Resource, reqparse


class Meal(Resource):

    def post(self, name):
        if MealModel.find_by_name(name):
            return {'message': 'This meal exists'}

        meal = MealModel(name)

        meal.save_to_db()
        return meal.json(), 201

    def delete(self, name):
        meal = MealModel.find_by_name(name)

        if meal:
            meal.delete_from_db()
            return {'message': 'Meal deleted successfully'}
        return {'message': 'Meal not found'}, 404


class ProductsToMeals(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product', type=str, required=True,
                        help='This field can not be empty')
    parser.add_argument('weight', type=int, required=True,
                        help='This field can not be empty')

    parser_to_delete = reqparse.RequestParser()
    parser_to_delete.add_argument('product', type=str, required=True,
                                  help='This field can not be empty')

    def get(self, name):
        meal = ProductsToMealsModel.find_by_name_all(name)
        calories = ProductsToMealsModel.calorie_count(meal)

        if meal:
            return {'Meal': name, 'Ingredients': [s.json_ingredients() for s in meal], "Calories of the meal": calories}
        return {'message': 'This meal does not exist'}, 404

    def post(self, name):
        data = ProductsToMeals.parser.parse_args()
        meal = ProductsToMealsModel(name, data['product'], data['weight'])
        meal_check = MealModel.find_by_name(name)
        ingredient_check_products_to_meals = ProductsToMealsModel.find_by_ingredient(
            name, data['product'])
        ingredient_check_groceries = FoodModel.find_by_foodstuff(
            data['product'])

        if meal_check:
            if ingredient_check_groceries:
                if ingredient_check_products_to_meals is None:
                    meal.save_to_db()
                    return meal.json(), 201
                return {'message': 'This ingredient exists'}
            return {'message': 'Ingredient does not exist database. Firstly, you have to create it.'}, 404
        return {'message': 'Meal does not exist. Firstly, you have to create it.'}, 404

    def delete(self, name):
        data = ProductsToMeals.parser_to_delete.parse_args()
        ingredient = ProductsToMealsModel.find_by_ingredient(
            name, data['product'])
        meal = ProductsToMealsModel.find_by_name(name)

        if meal:
            if ingredient:
                ingredient.delete_from_db()
                return {'message': 'Ingredient deleted successfully'}
            return {'message': 'Ingredient in the meal not found'}, 404
        return {'message': "Meal not found"}, 404

    def put(self, name):
        data = ProductsToMeals.parser.parse_args()
        meal = ProductsToMealsModel.find_by_name(name)
        ingredient = ProductsToMealsModel.find_by_ingredient(
            name, data['product'])

        if meal:
            if ingredient:
                ingredient.weight = data['weight']
                ingredient.save_to_db()
                return ingredient.json_ingredients(), 201
            return {'message': 'Ingredient in the meal not found'}, 404
        return {'message': 'Meal not found'}, 404


class MealsList(Resource):
    def get(self):
        return {'Favourite meals': [meal.name for meal in MealModel.query.all()]}
