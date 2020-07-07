#!/usr/bin/env python

import os
import sys
import glob
from app.tasks import import_zip

class ImportRecipes(object):
    def __init__(self):
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.recipes_files = os.path.join(self.basedir, 'recipes', '*.zip')

    def main(self):
        for index, zippath in enumerate(glob.glob(self.recipes_files)):
           import_zip.apply_async(args=[zippath], countdown=index*2)
        return 0

if __name__ == '__main__':
    sys.exit(ImportRecipes().main())
