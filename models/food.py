from database import db


class FoodModel(db.Model):
    __tablename__ = 'groceries'

    id = db.Column(db.Integer, primary_key=True)
    foodstuff = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    meal = db.relationship('ProductsToMealsModel',
                           backref='groceries', uselist=False)

    def __init__(self, foodstuff, calories):
        self.foodstuff = foodstuff
        self.calories = calories

    def json(self):
        return {'Ingredient': self.foodstuff, 'calories': self.calories}

    @classmethod
    def find_by_foodstuff(cls, foodstuff):
        return cls.query.filter(cls.foodstuff == foodstuff).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
