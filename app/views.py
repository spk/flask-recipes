from flask import render_template, request, url_for, redirect

from app import app, db
from models import Recipe

@app.route('/random')
def random():
    recipe = Recipe.random().first_or_404()
    return render_template('show.html', recipe=recipe)

@app.route('/<id>')
def show(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('show.html', recipe=recipe)

@app.route('/')
def index():
    query = Recipe.query
    page, per_page = get_page_items()
    pagination = query.order_by(Recipe.created_at.desc()).paginate(page, per_page)
    return render_template('index.html', pagination=pagination)

def get_page_items():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page')
    if not per_page:
        per_page = app.config.get('PER_PAGE', 10)
    else:
        per_page = int(per_page)
    return page, per_page
