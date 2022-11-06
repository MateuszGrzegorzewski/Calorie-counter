import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate
from dotenv import load_dotenv


from database import db
from resources.food import blp as FoodBlueprint
from resources.meals_fav import blp as FavoritesMealsBlueprint
from resources.time import blp as TimeBlueprint
from resources.daily_meals import blp as DailyMealsBlueprint
from resources.user import blp as UserBlueprint
from models.blocklist import Blocklist
from models.daily_meals import DailyMealsModel, ProductsToDailyMealsModel
from models.food import FoodModel
from models.meals_fav import MealModel, ProductsToMealsModel
from models.time import TimeModel
from models.user import UserModel


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    ACCESS_EXPIRES = timedelta(minutes=30)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Calorie Counter"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv(
        "DATABASE_URL", 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config["JWT_SECRET_KEY"] = "super-secret-password"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
    jwt = JWTManager(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = Blocklist.query.filter_by(jti=jti).scalar()

        return token is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.",
                    "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.",
                    "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @app.before_first_request
    def create_dates_in_tables():
        TimeModel.save_dates_to_db()
        DailyMealsModel.save_mealtimes_to_db()

    api.register_blueprint(FoodBlueprint)
    api.register_blueprint(FavoritesMealsBlueprint)
    api.register_blueprint(TimeBlueprint)
    api.register_blueprint(DailyMealsBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
