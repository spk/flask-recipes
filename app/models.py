from extensions import db
from datetime import datetime
from sqlalchemy.sql.expression import func
from sqlalchemy import event

categories = db.Table('recipes_categories',
        db.Column('category_id', db.Integer, db.ForeignKey('categories.id')),
        db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'))
        )

class Recipe(db.Model):
    __tablename__ = 'recipes'
    """
    Model for the Recipe created by the users.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), index=True)
    quantity = db.Column(db.String(15))
    directions = db.relationship('Direction', backref='Recipe',
            lazy='dynamic')
    ingredients = db.relationship('Ingredient', backref='Recipe',
            lazy='dynamic')
    categories = db.relationship('Category', secondary=categories,
            backref=db.backref('recipes', lazy='dynamic'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<%s>' % (self.title)

    @classmethod
    def random(self):
        return self.query.order_by(func.random()).limit(1)

class Direction(db.Model):
    __tablename__ = 'directions'
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Text)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.String(15))
    unit = db.Column(db.String(30))
    item = db.Column(db.Text, index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

# Trigers
def clean_title_before_insert(mapper, connection, target):
    target.title = target.title.replace('/', '')
    target.title = target.title.strip()

event.listen(Recipe, 'before_insert', clean_title_before_insert)
event.listen(Category, 'before_insert', clean_title_before_insert)
