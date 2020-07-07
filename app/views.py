from flask import render_template, request, jsonify, Blueprint

from .models import Recipe, Category
from .schemas import RecipeSchema, PaginationSchema

recipes = Blueprint("recipes", __name__)


@recipes.route('/api/v1/<int:id>')
def api_get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    result = RecipeSchema().dump(recipe)
    return jsonify(result)


@recipes.route('/api/v1/recipes', defaults={'page': 1})
@recipes.route('/api/v1/recipes/page/<int:page>')
def api_get_recipes(page):
    per_page = get_per_page()
    pagination = Recipe.query.order_by(
        Recipe.created_at.desc()).paginate(
        page, per_page)
    result = PaginationSchema().dump(pagination)
    return jsonify(result)


@recipes.route('/random')
def random():
    recipe = Recipe.random().first_or_404()
    return render_template('show.html', recipe=recipe)


@recipes.route('/<id>')
def show(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('show.html', recipe=recipe)


@recipes.route('/categories/', defaults={'page': 1})
@recipes.route('/categories/page/<int:page>')
def categories(page):
    per_page = get_per_page()
    pagination = Category.query.order_by(
        Category.created_at.desc()).paginate(
        page, per_page)
    return render_template('categories.html', pagination=pagination)


@recipes.route('/categories/<title>', defaults={'page': 1})
@recipes.route('/categories/<title>/page/<int:page>')
def recipes_by_category(title, page):
    per_page = get_per_page()
    pagination = Category.query.filter_by(
        title=title).first_or_404().recipes.paginate(
        page, per_page)
    return render_template('index.html', pagination=pagination)


@recipes.route('/', defaults={'page': 1})
@recipes.route('/page/<int:page>')
def index(page):
    per_page = get_per_page()
    pagination = Recipe.query.order_by(
        Recipe.created_at.desc()).paginate(
        page, per_page)
    return render_template('index.html', pagination=pagination)


def get_per_page():
    per_page = request.args.get('per_page')
    if not per_page:
        per_page = 10
    else:
        per_page = int(per_page)
    return per_page
