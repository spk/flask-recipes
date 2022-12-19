from flask import render_template, request, jsonify, Blueprint

from .extensions import db
from .models import Recipe, Category
from .schemas import RecipeSchema, PaginationSchema

recipes = Blueprint("recipes", __name__)

MAX_PER_PAGE = 1000


@recipes.route('/api/v1/<int:id>')
def api_get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    result = RecipeSchema().dump(recipe)
    return jsonify(result)


@recipes.route('/api/v1/recipes', defaults={'page': 1})
@recipes.route('/api/v1/recipes/page/<int:page>')
def api_get_recipes(page):
    pagination = db.paginate(
        db.select(Recipe).order_by(Recipe.created_at.desc()),
        page=page,
        max_per_page=MAX_PER_PAGE,
    )
    result = PaginationSchema().dump(pagination)
    return jsonify(result)


@recipes.route('/random')
def random():
    recipe = Recipe.random().first_or_404()
    return render_template('show.html', recipe=recipe)


@recipes.route('/recipes/<id>')
def show(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('show.html', recipe=recipe)


@recipes.route('/categories/', defaults={'page': 1})
@recipes.route('/categories/page/<int:page>')
def categories(page):
    pagination = db.paginate(
        db.select(Category).order_by(Category.created_at.desc()),
        page=page,
        max_per_page=MAX_PER_PAGE,
    )
    return render_template('categories.html', pagination=pagination)


@recipes.route('/categories/<title>', defaults={'page': 1})
@recipes.route('/categories/<title>/page/<int:page>')
def recipes_by_category(title, page):
    pagination = db.paginate(Category.query.filter_by(
        title=title
    ).first_or_404().recipes, page=page, max_per_page=MAX_PER_PAGE)
    return render_template('index.html', pagination=pagination)


@recipes.route('/', defaults={'page': 1})
@recipes.route('/page/<int:page>')
def index(page):
    pagination = db.paginate(
        db.select(Recipe).order_by(Recipe.created_at.desc()),
        page=page,
        max_per_page=MAX_PER_PAGE
    )
    return render_template('index.html', pagination=pagination)
