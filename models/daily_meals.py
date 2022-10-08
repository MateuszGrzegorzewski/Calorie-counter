from database import db
from models.time import TimeModel
from models.food import FoodModel


class DailyMealsModel(db.Model):
    __tablename__ = "mealtimes"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    mealtime = db.Column(db.String(100))

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
    def find_by_mealtime(cls, mealtime):
        return cls.query.filter_by(mealtime=mealtime).first()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).first()


class ProductsToDailyMealsModel(db.Model):
    __tablename__ = 'products_to_mealtimes'

    id = db.Column(db.Integer, primary_key=True)
    date_of_meal = db.Column(db.String(100))
    name_of_meal = db.Column(db.String(100))
    product = db.Column(db.String(100), db.ForeignKey('groceries.foodstuff'))
    weight = db.Column(db.Integer)

    def __init__(self, date_of_meal, name_of_meal, product, weight):
        self.date_of_meal = date_of_meal
        self.name_of_meal = name_of_meal
        self.product = product
        self.weight = weight

    def json(self):
        return {'date': self.date_of_meal, 'meal': self.name_of_meal, 'product': self.product, 'weight': self.weight}

    def json_ingredients(self):
        return {'product': self.product, 'weight': self.weight}

    @classmethod
    def find_by_date_and_name(cls, mealtime, date):
        return cls.query.filter_by(date_of_meal=date).filter_by(name_of_meal=mealtime).first()

    @classmethod
    def find_by_date_and_name_all(cls, mealtime, date):
        return cls.query.filter_by(name_of_meal=mealtime).filter_by(date_of_meal=date).all()

    @classmethod
    def find_by_ingredient(cls, mealtime, date, ingredient):
        return cls.query.filter_by(date_of_meal=date).filter_by(name_of_meal=mealtime).filter_by(product=ingredient).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def calorie_count(cls, meal):
        calories = 0
        for element in meal:
            calories_of_the_product = FoodModel.find_by_foodstuff(
                element.product).calories
            calories_of_the_meal = calories_of_the_product * element.weight / 100
            calories += calories_of_the_meal
        return calories
