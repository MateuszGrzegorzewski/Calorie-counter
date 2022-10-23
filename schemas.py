from marshmallow import Schema, fields


class FoodstuffSchema(Schema):
    id = fields.Int(dump_only=True)
    foodstuff = fields.Str(required=True)


class FoodSchema(FoodstuffSchema):
    calories = fields.Int(required=True)


class FoodUpdateSchema(Schema):
    foodstuff = fields.Str()
    calories = fields.Int()


class FavouriteMealSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ProductsToFavouriteMealSchema(Schema):
    meal = fields.Nested(FavouriteMealSchema(), dump_only=True)
    product_id = fields.Int(required=True, load_only=True)
    product = fields.Nested(FoodstuffSchema(), dump_only=True)
    weight = fields.Int(required=True)


class ProductsToFavouriteMealUpdateSchema(Schema):
    weight = fields.Int(required=True)


class DailyMealsSchema(Schema):
    product_id = fields.Int()
    product = fields.Nested(FoodstuffSchema(), dump_only=True)
    weight = fields.Int()
    favmeal_id = fields.Int()


class DailyMealsFavmealSchema(Schema):
    favmeal_id = fields.Int(required=True)


class DailyMealsUpdateSchema(Schema):
    weight = fields.Int(required=True)
