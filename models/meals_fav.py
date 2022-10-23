from database import db


class MealModel(db.Model):
    __tablename__ = 'meals-favourite'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)

    product_to_meals = db.relationship(
        'ProductsToMealsModel', back_populates="meal", lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class ProductsToMealsModel(db.Model):
    __tablename__ = 'products_to_favourite_meal'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    favmeal_id = db.Column(db.Integer, db.ForeignKey(
        'meals-favourite.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'groceries.id'), nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    product = db.relationship("FoodModel", back_populates="favmeal")
    meal = db.relationship("MealModel", back_populates="product_to_meals")

    def __init__(self, favmeal_id, product_id, weight):
        self.favmeal_id = favmeal_id
        self.product_id = product_id
        self.weight = weight

    @classmethod
    def find_product_in_meal_by_id(cls, favmeal_id, product_id):
        return cls.query.filter_by(favmeal_id=favmeal_id).filter_by(product_id=product_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def calorie_count(cls, favmeal_id):
        products = cls.query.filter_by(favmeal_id=favmeal_id).all()
        caloriess = 0
        for element in products:
            calories_of_the_product = element.product.calories
            calories_of_the_meal = calories_of_the_product * element.weight / 100
            caloriess += calories_of_the_meal
        return caloriess
