import zipfile
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app import create_celery_app
from flask import g
from .extensions import db
from .models import Recipe, Category, Ingredient, Direction

celery = create_celery_app()

def get_one_or_create(session, model, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        created = model(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one()

def new_recipe(root):
    title = root.find('recipe/head/title')
    try:
        quantity = root.find('recipe/head/yield').text.strip()
    except AttributeError:
        quantity = None

    cats = root.findall('recipe/head/categories/cat')
    cats_name = set([el.text for el in cats if el.text and len(el.text) > 1 and not el.text == 'None'])
    categories = []
    for cat in cats_name:
        category = get_one_or_create(db.session, Category, title=cat)
        categories.append(category)

    # XXX check ingredients validity (None)
    ings = root.findall('recipe/ingredients/ing')
    ingredients = []
    for ing in ings:
        quantity = ing.find('amt/qty').text
        u, unit = ing.find('amt/unit'), None
        if u is not None:
            unit = u.text
        item = ing.find('item').text
        ingredients.append(Ingredient(quantity=quantity, unit=unit, item=item))

    # XXX split paragraph when only one step
    steps = root.findall('recipe/directions/step')
    directions = []
    for step in steps:
        if step.text:
            directions.append(Direction(step=step.text.strip()))

    return Recipe(title=title.text,
            quantity=quantity,
            directions=directions,
            ingredients=ingredients,
            categories=categories)

@celery.task(bind=True)
def import_zip(self, zippath):
    with zipfile.ZipFile(zippath, 'r') as z:
        print("Import recipes from zip: {0}".format(zippath))
        filenames = z.namelist()
        for i, filename in enumerate(filenames, start=1):
            print("Import recipe: {0}".format(filename))
            try:
                content = z.open(filename).read()
                root = ET.fromstring(content)
                db.session.add(new_recipe(root))
                db.session.commit()
                self.update_state(state='PROGRESS',
                        meta={'current': i, 'total': len(filenames)})
            except ParseError:
                print("Error ! Last successful: {0}".format(filename))
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
        'result': "Import {0}".format(zippath)}
