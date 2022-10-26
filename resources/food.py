from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required

from models.food import FoodModel
from schemas import FoodSchema, FoodUpdateSchema


blp = Blueprint("food", __name__, description="Operations on groceries")


@blp.route("/food")
class Food(MethodView):
    @blp.response(200, FoodSchema(many=True))
    def get(self):
        food = FoodModel.query.all()
        return food

    @jwt_required()
    @blp.arguments(FoodSchema)
    @blp.response(201, FoodSchema)
    def post(self, food_data):
        try:
            food = FoodModel(food_data['foodstuff'], food_data['calories'])
            food.save_to_db()
            return food
        except IntegrityError:
            abort(409, message='Food already exists')


@blp.route("/food/<int:food_id>")
class Foodstuff(MethodView):
    @blp.response(200, FoodSchema)
    def get(self, food_id):
        food = FoodModel.query.get_or_404(food_id)
        return food

    @jwt_required()
    def delete(self, food_id):

        food = FoodModel.query.get_or_404(food_id)

        food.delete_from_db()
        return {"message": "Foodstuff deleted successfully"}, 200

    @jwt_required()
    @blp.arguments(FoodUpdateSchema)
    @blp.response(200, FoodSchema)
    def put(self, food_data, food_id):
        food = FoodModel.query.get(food_id)

        if food:
            food.foodstuff = food_data['foodstuff']
            food.calories = food_data['calories']
        else:
            food = FoodModel(**food_data)
            food.id = food_id

        food.save_to_db()
        return food
