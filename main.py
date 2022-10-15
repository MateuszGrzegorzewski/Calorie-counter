from flask import Flask
from flask_restful import Api
from resources.food import Food, Foodstuff
from resources.meals_fav import Meal, ProductsToMeals, MealsList
from models.time import TimeModel
from models.daily_meals import DailyMealsModel
from resources.time import Time
from resources.daily_meals import ProductsToDailyMeals, DailyMeals, ProductsToDailyMealsActual, DailyMealsActual
from database import db
import os

def create_app(db_url=None):
    app = Flask(__name__)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api = Api(app)


    @app.before_first_request
    def create_tables():
        db.create_all()


    @app.before_first_request
    def create_dates_in_tables():
        TimeModel.save_dates_to_db()
        DailyMealsModel.save_mealtimes_to_db()


    api.add_resource(Foodstuff, '/food/<string:foodstuff>')
    api.add_resource(Food, '/food')
    api.add_resource(Meal, '/fav-meal/<string:name>')
    api.add_resource(ProductsToMeals, '/fav-meal/products/<string:name>')
    api.add_resource(MealsList, '/fav-meal')
    api.add_resource(Time, "/time")
    api.add_resource(DailyMeals, '/daily-meals/<string:date>')
    api.add_resource(DailyMealsActual, '/daily-meals')
    api.add_resource(ProductsToDailyMeals,
                    '/daily-meals/products/<string:mealtime>/<string:date>')
    api.add_resource(ProductsToDailyMealsActual,
                    '/daily-meals/products/<string:mealtime>')

    return app
    
    # if __name__ == '__main__':
    #     db.init_app(app)
    #     app.run(port=5000, debug=True)
