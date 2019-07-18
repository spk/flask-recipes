# flask-recipes

Import recipes into flask web app.

## Install

### Standard

~~~ console
sudo apt install python-dev python-pip virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
~~~

Create database:

~~~ console
python db_manage.py up
~~~

~~~ console
python run.py || foreman start
~~~

Goto http://127.0.0.1:5000/

### Docker

~~~ console
docker-compose up
~~~

Run database creation command with:

~~~ console
docker-compose run app python db_manage.py up
~~~

## Import

~~~ console
sh download-recipes.sh
python import_recipes.py
~~~

## Tests

~~~ console
python tests.py
~~~

## Resources

* http://microformats.org/wiki/recipe-formats

## License

The MIT License

Copyright (c) 2015-2019 Laurent Arnoud <laurent@spkdev.net>
