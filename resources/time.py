from models.time import TimeModel
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

blp = Blueprint("Time", __name__, description="Getting the dates in database")

@blp.route("/time")
class Time(MethodView):
    @jwt_required()
    @blp.response(200)
    def get(self):
        return {"Available dates": [date.date for date in TimeModel.query.all()]}
