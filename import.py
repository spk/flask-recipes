#!/usr/bin/env python

import os
import sys
import zipfile
import glob
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from datetime import datetime
from app import app, db
from app.models import Recipe, Direction, Ingredient, Category

class ImportRecipes(object):
    def __init__(self):
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.recipes_files = os.path.join(self.basedir, 'recipes', '*.zip')
        self.create_db()

    def main(self):
        for zipname in glob.glob(self.recipes_files):
            with zipfile.ZipFile(zipname, 'r') as z:
                print("Import recipes from zip: {0}".format(zipname))
                for filename in z.namelist():
                    print("Import recipe: {0}".format(filename))
                    try:
                        content = z.open(filename).read()
                        root = ET.fromstring(content)
                        db.session.add(self.new_recipe(root))
                        db.session.commit()
                    except ParseError:
                        print("Error ! Last successful: {0}".format(filename))
        return 0

    def create_db(self):
        if not os.path.exists(os.path.join(self.basedir, 'app.db')):
            db.create_all()

    def new_recipe(self, root):
        title = root.find('recipe/head/title')

        cats = root.findall('recipe/head/categories/cat')
        categories = []
        for cat in cats:
            if cat.text and len(cat.text) > 1 and not cat.text == 'None':
                category = ImportRecipes.get_or_initialize(Category, title=cat.text.strip())
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

        return Recipe(title=title.text.strip(),
                directions=directions,
                ingredients=ingredients,
                categories=categories,
                created_at=datetime.utcnow())

    @classmethod
    def get_or_initialize(self, model, **kwargs):
        instance = model.query.filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            return instance


if __name__ == '__main__':
    sys.exit(ImportRecipes().main())
