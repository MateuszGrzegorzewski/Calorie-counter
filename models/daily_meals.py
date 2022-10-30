from flask_jwt_extended import get_jwt_identity
from database import db
from models.time import TimeModel


class DailyMealsModel(db.Model):
    __tablename__ = "mealtimes"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), db.ForeignKey('time.date'))
    mealtime = db.Column(db.String(100))

    time = db.relationship("TimeModel", back_populates="mealtimes")
    products = db.relationship(
        'ProductsToDailyMealsModel', back_populates='mealtimes', uselist=False)

    def __init__(self, date, mealtime):
        self.date = date
        self.mealtime = mealtime

    def save_mealtimes_to_db():
        for date in TimeModel.query.all():
            db.session.add(DailyMealsModel(date.date, 'breakfast'))
            db.session.add(DailyMealsModel(date.date, 'lunch'))
            db.session.add(DailyMealsModel(date.date, 'snack'))
            db.session.add(DailyMealsModel(date.date, 'dinner'))
            db.session.commit()

    @classmethod
    def find_by_date_and_mealtime(cls, date, mealtime):
        return cls.query.filter_by(date=date).filter_by(mealtime=mealtime).first()


class ProductsToDailyMealsModel(db.Model):
    __tablename__ = 'products_to_mealtimes'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_of_meal = db.Column(db.String(100), nullable=False)
    name_of_meal = db.Column(
        db.String(100), db.ForeignKey('mealtimes.mealtime'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'groceries.id'), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    mealtimes = db.relationship("DailyMealsModel", back_populates="products")
    food = db.relationship("FoodModel", back_populates="dailymeals")

    def __init__(self, date_of_meal, name_of_meal, product_id, weight, user_id):
        self.date_of_meal = date_of_meal
        self.name_of_meal = name_of_meal
        self.product_id = product_id
        self.weight = weight
        self.user_id = user_id

    def json_ingredients(self):
        return {'product_id': self.product_id, "product": self.food.foodstuff, 'weight': self.weight}

    @classmethod
    def find_by_date_and_mealtime(cls, date, mealtime):
        return cls.query.filter_by(user_id=get_jwt_identity()).filter_by(date_of_meal=date).filter_by(name_of_meal=mealtime).all()

    @classmethod
    def find_by_date_and_mealtime_one_element(cls, date, mealtime):
        return cls.query.filter_by(user_id=get_jwt_identity()).filter_by(date_of_meal=date).filter_by(name_of_meal=mealtime).first()

    @classmethod
    def find_by_product(cls, date, mealtime, product_id):
        return cls.query.filter_by(user_id=get_jwt_identity()).filter_by(date_of_meal=date).filter_by(name_of_meal=mealtime).filter_by(product_id=product_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def calorie_count(cls, mealtime, date):
        calories = 0
        meal = cls.find_by_date_and_mealtime(date, mealtime)
        for element in meal:
            calories_of_the_product = element.food.calories
            calories_of_the_meal = calories_of_the_product * element.weight / 100
            calories += calories_of_the_meal
        return calories
