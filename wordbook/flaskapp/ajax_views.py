"""Views used via javascript."""
from flask import jsonify
from flask import request
from flask import abort
from flask import Blueprint
from flask import current_app as app
from wordbook.domain import models as domain
from wordbook.domain.repo.translation import Repo as TranslationRepo
from wordbook.domain.repo.cardlist import CardlistRepo

ajax = Blueprint('ajax', __name__, url_prefix='/ajax')


@ajax.route('/_autocomplete-translations/<int:list_id>')
def translations_autocomplete(list_id):
    """Autocomplete for words and translations.

    The view receives the list_id parameter to be able to skip
    words that are already added do the list.

    .. http:post:: /ajax/_autocomplete-translations/<list_id>

       :statuscode 200: no error
    """
    try:
        query = request.args['query']
    except KeyError:
        app.logger.error('Insufficient parameters: %r', request.args)
        abort(400)

    translations = TranslationRepo().get_matching_translations(list_id, query)
    translations_dto = list(map(lambda t: t.dto_autocomplete(), translations))

    # Why not to use just an array?
    # http://flask.pocoo.org/docs/0.10/security/#json-security
    return jsonify(translations=translations_dto)


@ajax.route('/_create-new-card/<int:list_id>', methods=['POST'])
def create_new_card(list_id):
    """
    Add word translation to cardlist with given `list_id`.

    :query translation_id:

    :statuscode 200: no error
    :statuscode 400: insufficient query parameters
    """
    try:
        card = domain.Card(
            list_id=list_id,
            translation_id=request.form['translation_id']
        )
    except KeyError:
        app.logger.error('Insufficient parameters: %r', request.form)
        abort(400)

    card = CardlistRepo().add_card(card)
    translation = TranslationRepo().get(card.translation_id)
    return jsonify(card=card.dto(), translation=translation.dto_autocomplete())


@ajax.route('/_cards-on-list/<int:list_id>', methods=['GET'])
def cards_on_list(list_id):
    """Return words from the list.

    .. http:post:: /ajax/_cards-on-list/<list_id>

       :statuscode 200: no error
    """
    translations = CardlistRepo().get_cards_from_list(list_id)
    translations_dto = list(map(lambda t: t.dto_autocomplete(), translations))
    return jsonify(translations=translations_dto)


@ajax.route('/_add-translation', methods=['POST'])
def add_translation():
    """Add word with new translation.

    .. http:post:: /ajax/_add-translation

       :query word:
       :query ipa:
       :query simplified:
       :query translation:
       :query from_language:
       :query into_language:

       :statuscode 200: no error
       :statuscode 400: insufficient query parameters
    """
    try:
        translation = domain.Translation(
            from_language=request.form['from_language'],
            into_language=request.form['into_language'],
            word=request.form['word'],
            ipa=request.form['ipa'],
            simplified=request.form['simplified'],
            translated=request.form['translation']
        )
    except KeyError:
        app.logger.error('Insufficient parameters: %r', request.form)
        abort(400)
    else:
        app.logger.info('Translation: %s', translation.__dict__)
        translation = TranslationRepo().add_translation(translation)
    return jsonify(translation=translation.dto_autocomplete())
