from flask_restful import Resource, reqparse
from models.food import FoodModel
from models.daily_meals import DailyMealsModel, ProductsToDailyMealsModel
from resources.meals import ProductsToMeals
from datetime import date


class ProductsToDailyMeals(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product', type=str, required=True,
                        help='This field can not be empty')
    parser.add_argument('weight', type=int, required=True,
                        help='This field can not be empty')

    parser_to_delete = reqparse.RequestParser()
    parser_to_delete.add_argument('product', type=str, required=True,
                                  help='This field can not be empty')

    def get(self, mealtime, date=date.today()):
        meal_check = DailyMealsModel.find_by_mealtime(mealtime)
        date_check = DailyMealsModel.find_by_date(date)
        meal = ProductsToDailyMealsModel.find_by_date_and_name_all(
            mealtime, date)
        calories = ProductsToDailyMealsModel.calorie_count(meal)

        if date_check:
            if meal_check:
                return {'Date': date_check.date, 'Meal': meal_check.mealtime, 'Ingredients': [s.json_ingredients() for s in meal], "Calories of the meal": calories}
            return {'message': 'Mealtime is not exists. You can choose breakfast, lunch, snack or dinner'}
        return {'message': 'You write date in wrong way. Proper way is: yyyy-mm-dd. Example is 2022-10-08. It is also possible, that administrator does not upgrade data base'}

    def post(self, mealtime, date=date.today()):
        data = ProductsToDailyMeals.parser.parse_args()
        meal = ProductsToDailyMealsModel(
            date, mealtime, data['product'], data['weight'])
        meal_check = DailyMealsModel.find_by_mealtime(mealtime)
        date_check = DailyMealsModel.find_by_date(date)
        ingredient_check_products_to_meals = ProductsToDailyMealsModel.find_by_ingredient(
            mealtime, date, data['product'])
        ingredient_check_groceries = FoodModel.find_by_foodstuff(
            data['product'])

        if date_check:
            if meal_check:
                if ingredient_check_groceries:
                    if ingredient_check_products_to_meals is None:
                        meal.save_to_db()
                        return meal.json(), 201
                    return {'message': 'This ingredient exists'}
                return {'message': 'Ingredient does not exist in database. Firstly, you have to create it.'}, 404
            return {'message': 'Mealtime is not exists. You can choose breakfast, lunch, snack or dinner'}
        return {'message': 'You write date in wrong way. Proper way is: yyyy-mm-dd. Example is 2022-10-08. It is also possible, that administrator does not upgrade data base'}

    def delete(self, mealtime, date=date.today()):
        data = ProductsToDailyMeals.parser_to_delete.parse_args()
        meal_check = DailyMealsModel.find_by_mealtime(mealtime)
        date_check = DailyMealsModel.find_by_date(date)
        ingredient = ProductsToDailyMealsModel.find_by_ingredient(
            mealtime, date, data['product'])

        if date_check:
            if meal_check:
                if ingredient:
                    ingredient.delete_from_db()
                    return {'message': 'Ingredient deleted successfully'}
                return {'message': 'Ingredient in the meal not found'}, 404
            return {'message': 'Mealtime is not exists. You can choose breakfast, lunch, snack or dinner'}
        return {'message': 'You write date in wrong way. Proper way is: yyyy-mm-dd. Example is 2022-10-08. It is also possible, that administrator does not upgrade data base'}

    def put(self, mealtime, date=date.today()):
        data = ProductsToMeals.parser.parse_args()
        meal_check = DailyMealsModel.find_by_mealtime(mealtime)
        date_check = DailyMealsModel.find_by_date(date)
        ingredient = ProductsToDailyMealsModel.find_by_ingredient(
            mealtime, date, data['product'])

        if date_check:
            if meal_check:
                if ingredient:
                    ingredient.weight = data['weight']
                    ingredient.save_to_db()
                    return ingredient.json_ingredients(), 201
                return {'message': 'Ingredient in the meal not found'}, 404
            return {'message': 'Mealtime is not exists. You can choose breakfast, lunch, snack or dinner'}
        return {'message': 'You write date in wrong way. Proper way is: yyyy-mm-dd. Example is 2022-10-08. It is also possible, that administrator does not upgrade data base'}


class ProductsToDailyMealsActual(ProductsToDailyMeals):
    pass


class DailyMeals (Resource):
    def get(self, date=date.today()):
        date_check = DailyMealsModel.find_by_date(date)
        breakfast = ProductsToDailyMealsModel.find_by_date_and_name_all(
            'breakfast', date)
        calories_of_breakfast = ProductsToDailyMealsModel.calorie_count(
            breakfast)

        lunch = ProductsToDailyMealsModel.find_by_date_and_name_all(
            'lunch', date)
        calories_of_lunch = ProductsToDailyMealsModel.calorie_count(
            lunch)

        snack = ProductsToDailyMealsModel.find_by_date_and_name_all(
            'snack', date)
        calories_of_snack = ProductsToDailyMealsModel.calorie_count(
            snack)

        dinner = ProductsToDailyMealsModel.find_by_date_and_name_all(
            'dinner', date)
        calories_of_dinner = ProductsToDailyMealsModel.calorie_count(
            dinner)

        breakfast_json = {'Breakfast': [s.json_ingredients(
        ) for s in breakfast], 'Calories of the meal': calories_of_breakfast}
        lunch_json = {'Lunch': [s.json_ingredients(
        ) for s in lunch], 'Calories of the meal': calories_of_lunch}
        snack_json = {'Snack': [s.json_ingredients(
        ) for s in snack], 'Calories of the meal': calories_of_snack}
        dinner_json = {'Dinner': [s.json_ingredients(
        ) for s in dinner], 'Calories of the meal': calories_of_dinner}
        date_json = {'Date': date_check.date}
        sum_of_calories_json = {'Calories of the day': calories_of_breakfast +
                                calories_of_lunch+calories_of_snack+calories_of_dinner}

        if date_check:
            return date_json, sum_of_calories_json, breakfast_json, lunch_json, snack_json, dinner_json
        return {'message': 'You write date in wrong way. Proper way is: yyyy-mm-dd. Example is 2022-10-08. It is also possible, that administrator does not upgrade data base'}


class DailyMealsActual(DailyMeals):
    pass
