import zipfile
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app import create_celery_app
from .extensions import db
from .models import Recipe, Category, Ingredient, Direction

celery = create_celery_app()


def new_recipe(root):
    title = root.find('recipe/head/title')
    try:
        quantity = root.find('recipe/head/yield').text.strip()
    except AttributeError:
        quantity = None

    categories = root.findall('recipe/head/categories/cat')
    categorie_names = set([el.text for el in categories if el.text and len(
        el.text) > 1 and not el.text == 'None'])
    categories = []
    for categorie_name in categorie_names:
        clean_title = categorie_name.replace('/', '').strip()
        category = db.session.query(Category).filter_by(
            title=clean_title).first()
        if category is None:
            category = Category(title=clean_title)
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


@celery.task(bind=True, default_retry_delay=5)
def import_recipe(self, xml_content):
    try:
        root = ET.fromstring(xml_content)
        db.session.add(new_recipe(root))
        db.session.commit()
    except ParseError:
        print("ParseError in: {0}".format(xml_content))
        db.session.rollback()
    except IntegrityError as exc:
        print("IntegrityError in: {0}".format(xml_content))
        db.session.rollback()
        raise self.retry(exc=exc)
    finally:
        db.session.close()


@celery.task(bind=True)
def import_zip(self, zippath):
    with zipfile.ZipFile(zippath, 'r') as z:
        print("Import recipes from zip: {0}".format(zippath))
        filenames = z.namelist()
        for i, filename in enumerate(filenames, start=1):
            print("Import recipe: {0}".format(filename))
            xml_content = z.open(filename).read()
            import_recipe.delay(xml_content.decode('utf-8'))
            self.update_state(state='PROGRESS',
                              meta={'current': i, 'total': len(filenames)})
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': "Import {0}".format(zippath)}
