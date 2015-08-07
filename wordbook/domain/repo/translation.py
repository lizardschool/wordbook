import logging
from sqlalchemy.orm.exc import NoResultFound
from . import base
from wordbook.infra.models.word import Word
from wordbook.infra.models.translation import Translation
from wordbook.domain import models as domain

log = logging.getLogger(__name__)

__all__ = ('Repo', )


class Repo(base.DbRepo):
    def get_matching_translations(self, list_id, query):
        """Get translations matching given language and fragment of the word.

        :param int list_id:
        :param string query:

        :returns: List of translations
        :rtype: []domain.Translation
        """
        assert isinstance(query, str)
        # TODO: language as subquery
        # TODO: exclude words existing already at list
        language = 'en'

        query = self.session.query(Word, Translation).join(Translation).filter(
            Word.language == language).filter(
            Word.word.ilike('%{}%'.format(query))
        ).order_by(Word.word, Translation.translation)

        for word, translation in query.all():
            yield domain.Translation(
                id=translation.id,
                from_language=word.language,
                into_language=translation.language,
                word=word.word,
                ipa=word.ipa,
                simplified=word.simplified_pronunciation,
                translated=translation.translation
            )

    def _get_or_create_word(self, language, word, ipa, simplified_pronunciation):
        query = self.session.query(Word).filter_by(
            language=language,
            word=word)

        try:
            word = query.one()
        except NoResultFound:
            word = Word(
                language=language,
                word=word,
                ipa=ipa,
                simplified_pronunciation=simplified_pronunciation)

            self.session.add(word)
            self.session.commit()

        return word

    def get(self, translation_id):
        query = self.session.query(Translation).filter_by(id=translation_id)
        row = query.one()
        translation = domain.Translation(
            id=row.id,
            from_language=row.word.language,
            into_language=row.language,
            word=row.word.word,
            ipa=row.word.ipa,
            simplified=row.word.simplified_pronunciation,
            translated=row.translation
        )
        return translation

    def _get_or_create_translation(self, word, to_language, translated):
        assert isinstance(word, Word)
        query = self.session.query(Translation).filter_by(
            word_id=word.id,
            language=to_language,
            translation=translated)

        try:
            translation = query.one()
        except NoResultFound:
            translation = Translation(
                language=to_language,
                translation=translated,
                word_id=word.id)

            self.session.add(translation)
            self.session.commit()

        return translation

    def add_translation(self, translation):
        assert isinstance(translation, domain.Translation)
        word = self._get_or_create_word(
            translation.from_language,
            translation.word,
            translation.ipa,
            translation.simplified)

        db_translation = self._get_or_create_translation(
            word,
            translation.into_language,
            translation.translated)

        translation.id = db_translation.id
        return translation
