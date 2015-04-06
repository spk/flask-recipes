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
        for zippath in glob.glob(self.recipes_files):
           import_zip.delay(zippath)
        return 0

if __name__ == '__main__':
    sys.exit(ImportRecipes().main())
