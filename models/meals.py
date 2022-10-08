from database import db
from models.food import FoodModel


class MealModel(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    product_to_meals = db.relationship(
        'ProductsToMealsModel', backref='meals', uselist=False)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'meal': self.name}
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class ProductsToMealsModel(db.Model):
    __tablename__ = 'products_to_meals'

    id = db.Column(db.Integer, primary_key=True)
    name_of_meal = db.Column(db.String(255), db.ForeignKey('meals.name'))
    product = db.Column(db.String(100), db.ForeignKey('groceries.foodstuff'))
    weight = db.Column(db.Integer)

    def __init__(self, name_of_meal, product, weight):
        self.name_of_meal = name_of_meal
        self.product = product
        self.weight = weight

    def json(self):
        return {'meal': self.name_of_meal, 'product': self.product, 'weight': self.weight}

    def json_ingredients(self):
        return {'product': self.product, 'weight': self.weight}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name_of_meal=name).first()

    @classmethod
    def find_by_name_all(cls, name):
        return cls.query.filter_by(name_of_meal=name).all()

    @classmethod
    def find_by_ingredient(cls, name, ingredient):
        return cls.query.filter_by(name_of_meal=name).filter_by(product=ingredient).first()

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
