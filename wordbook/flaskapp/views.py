from flask import Blueprint
from flask import render_template
from wordbook.domain import models as domain
from wordbook.domain.repo.cardlist import CardlistRepo

frontend = Blueprint('frontend', __name__, url_prefix='')


@frontend.route('/')
def index():
    return "Hello, World!"


@frontend.route('/list/<list_hash>')
def show_list(list_hash):
    list_id = domain.List.hash2id(list_hash)
    translations = list(CardlistRepo().get_translations(list_id))
    return render_template(
        'frontend/show_list.html',
        translations=translations)
