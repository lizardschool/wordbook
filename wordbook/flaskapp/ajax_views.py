from flask import jsonify
from flask import request
from flask import abort
from . import app
from wordbook.domain import models as domain
from wordbook.domain.repo.translation import Repo as TranslationRepo
from wordbook.domain.repo.cardlist import CardlistRepo


@app.route('/_autocomplete-translations/<int:list_id>')
def translations_autocomplete(list_id):
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


@app.route('/_create-new-card/<list_id>', methods=['POST'])
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
            translation_id=request.args['translation_id']
        )
    except KeyError:
        app.logger.error('Insufficient parameters: %r', request.args)
        abort(400)

    card = CardlistRepo().add_card(card)
    translation = TranslationRepo().get(card.translation_id)
    return jsonify(card=card.dto(), translation=translation.dto_autocomplete())


@app.route('/_cards-on-list/<list_id>', methods=['GET'])
def cards_on_list(list_id):
    translations = CardlistRepo().get_translations(list_id)
    translations_dto = list(map(lambda t: t.dto_autocomplete(), translations))
    return jsonify(translations=translations_dto)


@app.route('/_add-translation', methods=['POST'])
def add_translation():
    """

    .. http:post:: /_add-translation

       :query word:
       :query ipa:
       :query translation:
       :query from_language:
       :query into_language:

       :statuscode 200: no error
       :statuscode 400: insufficient query parameters
    """
    try:
        translation = domain.Translation(
            from_language=request.form['from_language'],
            into_languege=request.form['into_language'],
            word=request.form['word'],
            ipa=request.form['ipa'],
            translated=request.form['translation']
        )
    except KeyError:
        app.logger.error('Insufficient parameters: %r', request.args)
        abort(400)
    else:
        translation = TranslationRepo().add_translation(translation)
    return jsonify(translation=translation.dto_autocomplete())
