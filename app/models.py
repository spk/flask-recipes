from app import db
from sqlalchemy.sql.expression import func

categories = db.Table('categories',
        db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
        db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
        )

class Recipe(db.Model):
    """
    Model for the Recipe created by the users.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True)
    directions = db.relationship('Direction', backref='Recipe',
            lazy='dynamic')
    ingredients = db.relationship('Ingredient', backref='Recipe',
            lazy='dynamic')
    categories = db.relationship('Category', secondary=categories,
            backref=db.backref('recipes', lazy='dynamic'))
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<%s>' % (self.title)

    @classmethod
    def random(self):
        return self.query.order_by(func.random()).limit(1)

class Direction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Text)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    unit = db.Column(db.String(30))
    item = db.Column(db.String(30), index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True)
