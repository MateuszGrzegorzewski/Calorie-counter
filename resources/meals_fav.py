from sqlalchemy.exc import IntegrityError
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.meals_fav import MealModel, ProductsToMealsModel
from schemas import FavouriteMealSchema, ProductsToFavouriteMealSchema, ProductsToFavouriteMealUpdateSchema
from models.food import FoodModel

blp = Blueprint("Favourite meals", __name__,
                description="Operations on favourite meals")


@blp.route('/fav-meal')
class MealsList(MethodView):
    @jwt_required()
    @blp.response(200, FavouriteMealSchema(many=True))
    def get(self):
        favmeals = MealModel.query.filter_by(user_id=get_jwt_identity()).all()
        return favmeals

    @jwt_required()
    @blp.arguments(FavouriteMealSchema)
    @blp.response(201, FavouriteMealSchema)
    def post(self, meal_data):
        unique_check = MealModel.query.filter_by(
            user_id=get_jwt_identity()).filter_by(name=meal_data['name']).first()

        if unique_check is not None:
            abort(404, message="Favourite meal already exists.")

        try:
            favmeal = MealModel(
                name=meal_data['name'], user_id=get_jwt_identity())
            favmeal.save_to_db()
            return favmeal
        except IntegrityError:
            abort(409, message="Error occured while trying to create favourite meal.")


@blp.route("/fav-meal/<int:favmeal_id>")
class Meal(MethodView):
    @jwt_required()
    def delete(self, favmeal_id):
        meal = MealModel.query.get_or_404(favmeal_id)
        products_in_meal = ProductsToMealsModel.query.filter_by(
            favmeal_id=favmeal_id).all()
        check_products_in_meal = ProductsToMealsModel.query.filter_by(
            favmeal_id=favmeal_id).first()

        if check_products_in_meal is not None:
            for product in products_in_meal:
                product.delete_from_db()

        if meal.user_id != get_jwt_identity():
            abort(401, message="No authorisation to access this data")

        meal.delete_from_db()
        return {'message': 'Favourite meal deleted successfully'}, 200


@blp.route('/fav-meal/products/<int:favmeal_id>')
class ProductsToMealsList(MethodView):
    @jwt_required()
    def get(self, favmeal_id):
        meals = ProductsToMealsModel.query.filter_by(
            favmeal_id=favmeal_id).all()
        meal = ProductsToMealsModel.query.filter_by(
            favmeal_id=favmeal_id).first()

        if meal is None:
            abort(404, message="Informations not found")

        if meal.meal.user_id != get_jwt_identity():
            abort(401, message="No authorisation to access this data")

        calories = ProductsToMealsModel.calorie_count(favmeal_id)

        try:
            return {"Favourite meal - id": favmeal_id, "Favourite meal": meal.meal.name, "Products": [{"Product": e.product.foodstuff, "Weight": e.weight} for e in meals], "Calories": calories}
        except AttributeError:
            abort(500, message="Error occured while trying to get favmeal")

    @blp.arguments(ProductsToFavouriteMealSchema)
    @blp.response(201, ProductsToFavouriteMealSchema)
    @jwt_required()
    def post(self, product_data, favmeal_id):
        favmeal = MealModel.query.filter_by(
            id=favmeal_id).first()
        if favmeal is None:
            abort(404, message="Favourite meal not found")

        if favmeal.user_id != get_jwt_identity():
            abort(401, message="No authorisation to access this data")

        check_product_in_food = FoodModel.query.filter_by(
            id=product_data['product_id']).first()

        if check_product_in_food is None:
            abort(404, message="Product not found in database")

        check_product_by_id = ProductsToMealsModel.find_product_in_meal_by_id(
            favmeal_id, product_data['product_id'])

        if check_product_by_id:
            abort(409, message="The product already exists in this meal.")

        try:
            product = ProductsToMealsModel(favmeal_id, **product_data)
            product.save_to_db()
            return product
        except IntegrityError:
            abort(
                500, message="Error occured while trying to add a product")


@blp.route('/fav-meal/products/<int:favmeal_id>/<int:product_id>')
class ProductsToMeals(MethodView):
    @jwt_required()
    def delete(self, favmeal_id, product_id):
        product = ProductsToMealsModel.find_product_in_meal_by_id(
            favmeal_id, product_id)

        if product is None:
            abort(404, message="Meal or the product in the meal or both not found.")

        if product.meal.user_id != get_jwt_identity():
            abort(401, message="No authorisation to access this data")

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

        if product.meal.user_id != get_jwt_identity():
            abort(401, message="No authorisation to access this data")

        product.weight = product_data['weight']
        product.save_to_db()
        return product
