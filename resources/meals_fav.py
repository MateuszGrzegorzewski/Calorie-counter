from sqlalchemy.exc import IntegrityError
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from models.meals_fav import MealModel, ProductsToMealsModel
from schemas import FavouriteMealSchema, ProductsToFavouriteMealSchema, ProductsToFavouriteMealUpdateSchema


blp = Blueprint("Favourite meals", __name__,
                description="Operations on favourite meals")


@blp.route('/fav-meal')
class MealsList(MethodView):
    @blp.response(200, FavouriteMealSchema(many=True))
    def get(self):
        favmeals = MealModel.query.all()
        return favmeals

    @jwt_required()
    @blp.arguments(FavouriteMealSchema)
    @blp.response(201, FavouriteMealSchema)
    def post(self, meal_data):
        try:
            favmeal = MealModel(**meal_data)
            favmeal.save_to_db()
            return favmeal
        except IntegrityError:
            abort(409, message="Favourite meal already exists")


@blp.route("/fav-meal/<string:favmeal_id>")
class Meal(MethodView):
    @jwt_required()
    def delete(self, favmeal_id):
        meal = MealModel.query.get_or_404(favmeal_id)

        meal.delete_from_db()
        return {'message': 'Favourite meal deleted successfully'}, 200


@blp.route('/fav-meal/products/<string:favmeal_id>')
class ProductsToMealsList(MethodView):
    def get(self, favmeal_id):
        meals = ProductsToMealsModel.query.filter_by(
            favmeal_id=favmeal_id).all()
        meal = ProductsToMealsModel.query.filter_by(
            favmeal_id=favmeal_id).first()

        try:
            calories = ProductsToMealsModel.calorie_count(favmeal_id)
        except AttributeError:
            abort(500, message="Error occured, Probably you have products in meals, which are not in food database")

        return {"Favmeal Id": favmeal_id, "Favmeal": meal.meal.name, "Products": [{"Product": e.product.foodstuff, "Weight": e.weight} for e in meals], "Calories": calories}

    @blp.arguments(ProductsToFavouriteMealSchema)
    @blp.response(201, ProductsToFavouriteMealSchema)
    @jwt_required()
    def post(self, product_data, favmeal_id):
        check_product_by_id = ProductsToMealsModel.find_product_in_meal_by_id(
            favmeal_id, product_data['product_id'])

        if check_product_by_id:
            abort(409, message="The product already exists in this meal.")

        try:
            product = ProductsToMealsModel(
                favmeal_id, **product_data)
            product.save_to_db()
            return product
        except IntegrityError:
            abort(
                500, message="Error occured during adding a product")


@blp.route('/fav-meal/products/<string:favmeal_id>/<string:product_id>')
class ProductsToMeals(MethodView):
    @jwt_required()
    def delete(self, favmeal_id, product_id):
        product = ProductsToMealsModel.find_product_in_meal_by_id(
            favmeal_id, product_id)

        if product is None:
            abort(404, message="Meal or the product in the meal or both not found.")

        product.delete_from_db()
        return {"message": "Product deleted successfully"}, 200

    @jwt_required()
    @blp.arguments(ProductsToFavouriteMealUpdateSchema)
    @blp.response(200, ProductsToFavouriteMealSchema)
    def put(self, product_data, favmeal_id, product_id):
        product = ProductsToMealsModel.find_product_in_meal_by_id(
            favmeal_id, product_id)

        if product is None:
            abort(404, message="Meal or the product in the meal or both not found.")

        product.weight = product_data['weight']
        product.save_to_db()
        return product
