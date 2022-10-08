from models.time import TimeModel
from flask_restful import Resource


class Time(Resource):
    def get(self):
        return {"Available dates": [date.date for date in TimeModel.query.all()]}
