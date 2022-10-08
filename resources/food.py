from models.food import FoodModel
from flask_restful import Resource, reqparse


class Food(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('foodstuff', type=str,
                        required=True, help="This field can not be empty")
    parser.add_argument('calories', type=int,
                        required=True, help="This field can not be empty")

    parser_to_delete = reqparse.RequestParser()
    parser_to_delete.add_argument('foodstuff', type=str,
                                  required=True, help="This field can not be empty")

    def get(self):
        return {'groceries': [food.json() for food in FoodModel.query.all()]}

    def post(self):
        data = Food.parser.parse_args()

        if FoodModel.find_by_foodstuff(data['foodstuff']):
            return {'message': 'This food is already exist'}

        food = FoodModel(data['foodstuff'], data['calories'])
        food.save_to_db()
        return food.json(), 201

    def delete(self):
        data = Food.parser_to_delete.parse_args()
        food = FoodModel.find_by_foodstuff(data['foodstuff'])

        if food:
            food.delete_from_db()
        else:
            return {'message': 'Food is not exist'}, 404
        return {'message': 'This food has been deleted'}

    def put(self):
        data = Food.parser.parse_args()

        food = FoodModel.find_by_foodstuff(data['foodstuff'])

        if food is None:
            food = FoodModel(data['foodstuff'], data['calories'])
        else:
            food.calories = data['calories']

        food.save_to_db()
        return food.json(), 201


class Foodstuff(Resource):
    def get(self, foodstuff):
        food = FoodModel.find_by_foodstuff(foodstuff)

        if food:
            return food.json()
        return {'message': 'This food is not exist'}, 404
