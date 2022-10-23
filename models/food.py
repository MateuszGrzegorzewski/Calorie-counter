from database import db


class FoodModel(db.Model):
    __tablename__ = 'groceries'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    foodstuff = db.Column(db.String(100), unique=True, nullable=False)
    calories = db.Column(db.Integer, nullable=False)

    favmeal = db.relationship('ProductsToMealsModel',
                              uselist=False, back_populates="product")
    dailymeals = db.relationship(
        'ProductsToDailyMealsModel', uselist=False, back_populates="food")

    def __init__(self, foodstuff, calories):
        self.foodstuff = foodstuff
        self.calories = calories

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
