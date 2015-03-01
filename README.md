# flask-recipes

Import [RecipeML](http://www.formatdata.com/recipeml/spec/recipeml-spec.html)
[recipes](http://dsquirrel.tripod.com/recipeml/indexrecipes2.html) into sample
web app.

## Install

~~~ console
sudo apt install python-dev python-pip virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
~~~

Start `python` console:

~~~ console
from app import db
db.create_all()
~~~

~~~ console
python run.py || foreman start
~~~

## Import

~~~ console
sh download-recipes.sh
python import.py
~~~

Goto http://127.0.0.1:5000/

## License

The MIT License

Copyright (c) 2015 Laurent Arnoud <laurent@spkdev.net>
