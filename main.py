from flask import Flask
from flask_smorest import Api
from models.time import TimeModel
from models.daily_meals import DailyMealsModel
from database import db

from resources.food import blp as FoodBlueprint
from resources.meals_fav import blp as FavoritesMealsBlueprint
from resources.time import blp as TimeBlueprint
from resources.daily_meals import blp as DailyMealsBlueprint


app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Calorie Counter"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.before_first_request
def create_dates_in_tables():
    if TimeModel.query.first() is None:
        TimeModel.save_dates_to_db()
        DailyMealsModel.save_mealtimes_to_db()
    else:
        pass


api.register_blueprint(FoodBlueprint)
api.register_blueprint(FavoritesMealsBlueprint)
api.register_blueprint(TimeBlueprint)
api.register_blueprint(DailyMealsBlueprint)
