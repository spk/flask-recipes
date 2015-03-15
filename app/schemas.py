from marshmallow import Schema, fields

class RecipeSchema(Schema):
    directions = fields.Nested('DirectionSchema', many=True)
    ingredients = fields.Nested('IngredientSchema', many=True)
    categories = fields.Nested('CategorySchema', many=True)
    class Meta:
        fields = ('id', 'title', 'quantity', 'created_at',
                'directions', 'ingredients', 'categories')

class DirectionSchema(Schema):
    class Meta:
        fields = ('step', )

class IngredientSchema(Schema):
    class Meta:
        fields = ('quantity', 'unit', 'item')

class CategorySchema(Schema):
    class Meta:
        fields = ('title', )

# https://pythonhosted.org/Flask-SQLAlchemy/api.html#flask.ext.sqlalchemy.Pagination
class PaginationSchema(Schema):
    items = fields.Nested('RecipeSchema', many=True)
    class Meta:
        fields = ('has_next', 'has_prev', 'items', 'page',
                'pages', 'per_page', 'total')
