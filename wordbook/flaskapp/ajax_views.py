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


@ajax.route('/autocomplete-cards')
def cards_autocomplete():
    """Autocomplete for words from cards.

    The view receives the list_id parameter to be able to skip
    words that are already added do the list.

    .. http:post:: /ajax/autocomplete-cards

       :query list_id: list identifier
       :query query: Autocoplete query

       :statuscode 200: no error
       :statuscode 400: insufficient or invalid parameters
    """

    try:
        list_id = int(request.args['list_id'])
        query = request.args['query']
    except KeyError:
        app.logger.error('Insufficient parameters: %r', request.args)
        abort(400)
    except ValueError:
        app.logger.error('Invalid parameters: %r', request.args)
        abort(400)

    raise NotImplementedError
    translations = TranslationRepo().get_matching_translations(list_id, query)
    translations_dto = list(map(lambda t: t.dto_autocomplete(), translations))

    # Why not to use just an array?
    # http://flask.pocoo.org/docs/0.10/security/#json-security
    return jsonify(translations=translations_dto)


@ajax.route('/create-new-card/<int:list_id>', methods=['POST'])
def create_new_card(list_id):
    """
    Add word translation to cardlist with given `list_id`.

    .. http:post:: /ajax/create-new-card/<int:list_id>

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


@ajax.route('/cards-on-list/<int:list_id>')
def cards_on_list(list_id):
    """Return words from the list.

    .. http:post:: /ajax/cards-on-list/<int:list_id>

       :statuscode 200: no error
    """
    cards = CardlistRepo().get_cards_from_list(list_id)
    # TODO: card DTO is not implemented
    cards_dto = list(map(lambda card: card.dto_autocomplete(), cards))
    return jsonify(cards=cards_dto)


@ajax.route('/add-translation', methods=['POST'])
def add_translation():
    """Add word with new translation.

    .. http:post:: /ajax/add-translation

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
