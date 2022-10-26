from datetime import date
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required

from models.daily_meals import DailyMealsModel, ProductsToDailyMealsModel
from models.meals_fav import ProductsToMealsModel as ProductsOfFavouriteMeal, MealModel
from schemas import DailyMealsSchema, DailyMealsUpdateSchema, DailyMealsFavmealSchema


blp = Blueprint("DailyMeals", __name__,
                description="Operations on daily meals")


@blp.route('/daily-meals/products/<string:mealtime>/<string:date>')
class ProductsToDailyMeals(MethodView):
    @jwt_required()
    def get(self, mealtime, date=date.today()):
        meal = ProductsToDailyMealsModel.find_by_date_and_mealtime(
            date, mealtime)
        calories = ProductsToDailyMealsModel.calorie_count(mealtime, date)

        return {'Date': date.strftime('%Y-%m-%d'), 'Meal': mealtime, 'Products': [{"Product": e.food.foodstuff, "Weight": e.weight} for e in meal], "Calories of the meal": calories}

    @jwt_required()
    @blp.arguments(DailyMealsSchema)
    def post(self, mealtime_data, mealtime, date=date.today()):
        if DailyMealsModel.find_by_date_and_mealtime(date, mealtime) is None:
            abort(
                404, message="Date or mealtime or both not found. Check that the entered values are correct")

        if ProductsToDailyMealsModel.find_by_product(date, mealtime, mealtime_data['product_id']):
            abort(409, message="The product already exists in this mealtime")

        try:
            meal = ProductsToDailyMealsModel(
                date, mealtime, mealtime_data['product_id'], mealtime_data['weight'])
            meal.save_to_db()
            return {"Product_id": meal.product_id, "Product": meal.food.foodstuff, "Weight": meal.weight}, 201
        except IntegrityError:
            abort(500, message="Error occured during adding a product")


@blp.route('/daily-meals/products/<string:mealtime>/<string:date>/favmeal')
class FavmealsToDailyMeals(MethodView):
    @jwt_required()
    @blp.arguments(DailyMealsFavmealSchema)
    def post(self, mealtime_data, mealtime, date=date.today()):
        favmeal = MealModel.query.get_or_404(mealtime_data['favmeal_id'])
        favmeals = ProductsOfFavouriteMeal.query.filter_by(
            favmeal_id=favmeal.id).all()

        added_products = []

        for product in favmeals:
            if ProductsToDailyMealsModel.find_by_product(date, mealtime, product.product_id):
                continue
            try:
                meal = ProductsToDailyMealsModel(
                    date, mealtime, product.product_id, product.weight)
                meal.save_to_db()
            except IntegrityError:
                abort(500, message="Error occured during adding a product")

            added_products.append({"product_id": meal.product_id,
                                   "product": meal.food.foodstuff, "weight": meal.weight})

        return {"Added products": added_products}, 201


@blp.route('/daily-meals/products/<string:mealtime>/<string:date>/<string:product_id>')
class ProductOfDailyMeals(MethodView):
    @jwt_required()
    def delete(self, mealtime, date=date.today(), product_id=None):
        product = ProductsToDailyMealsModel.find_by_product(
            date, mealtime, product_id)

        if product is None:
            abort(404, message="Product not found in this mealtime")

        product.delete_from_db()
        return {'message': "Product deleted successfully"}

    @blp.arguments(DailyMealsUpdateSchema)
    @jwt_required()
    def put(self, mealtime_data, mealtime, date=date.today(), product_id=None):
        product = ProductsToDailyMealsModel.find_by_product(
            date, mealtime, product_id)

        if product is None:
            abort(404, message="Product not found in this mealtime")

        product.weight = mealtime_data['weight']
        product.save_to_db()
        return {"Product_id": product.product_id, "Product": product.food.foodstuff, "Weight": product.weight}


@blp.route('/daily-meals/products/<string:mealtime>')
class ProductsToDailyMealsActual(ProductsToDailyMeals):
    pass


@blp.route('/daily-meals/products/<string:mealtime>/favmeal')
class FavmealsToDailyMealsActual(FavmealsToDailyMeals):
    pass


@blp.route('/daily-meals/products/<string:mealtime>/<string:product_id>')
class ProductOfDailyMealsActual(ProductOfDailyMeals):
    pass


@blp.route('/daily-meals/<string:date>')
class DailyMeals (MethodView):
    @jwt_required()
    def get(self, date=date.today()):
        breakfast = ProductsToDailyMealsModel.find_by_date_and_mealtime(
            date, 'breakfast')
        calories_of_breakfast = ProductsToDailyMealsModel.calorie_count(
            'breakfast', date)
        lunch = ProductsToDailyMealsModel.find_by_date_and_mealtime(
            date, 'lunch')
        calories_of_lunch = ProductsToDailyMealsModel.calorie_count(
            'lunch', date)
        snack = ProductsToDailyMealsModel.find_by_date_and_mealtime(
            date, 'snack')
        calories_of_snack = ProductsToDailyMealsModel.calorie_count(
            'snack', date)
        dinner = ProductsToDailyMealsModel.find_by_date_and_mealtime(
            date, 'dinner')
        calories_of_dinner = ProductsToDailyMealsModel.calorie_count(
            'dinner', date)

        breakfast_json = {'Breakfast': [s.json_ingredients(
        ) for s in breakfast], 'Calories of the meal': calories_of_breakfast}
        lunch_json = {'Lunch': [s.json_ingredients(
        ) for s in lunch], 'Calories of the meal': calories_of_lunch}
        snack_json = {'Snack': [s.json_ingredients(
        ) for s in snack], 'Calories of the meal': calories_of_snack}
        dinner_json = {'Dinner': [s.json_ingredients(
        ) for s in dinner], 'Calories of the meal': calories_of_dinner}

        total_calories = calories_of_breakfast + \
            calories_of_lunch+calories_of_snack+calories_of_dinner

        return {'Date': date.strftime('%Y-%m-%d'), 'Calories of the day': total_calories, "Meals": [breakfast_json, lunch_json, snack_json, dinner_json]}


@blp.route('/daily-meals')
class DailyMealsActual(DailyMeals):
    pass
