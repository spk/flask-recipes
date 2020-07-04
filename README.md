# flask-recipes

Import recipes into flask web app.

## Setup

```
sudo apt install python-dev python-pip virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create database:

```
python db_manage.py up
```

Run:

```
python run.py || foreman start
```

Goto http://127.0.0.1:5000/

## Import

```
celery worker --app=app.tasks
sh download-recipes.sh
python import_recipes.py
```

## Tests

```
pytest
```

## Resources

* http://microformats.org/wiki/recipe-formats

## License

The MIT License

Copyright (c) 2015-2020 Laurent Arnoud <laurent@spkdev.net>
