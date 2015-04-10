from sqlalchemy.orm.exc import NoResultFound
from . import base
from wordbook.infra.models.word import Word
from wordbook.infra.models.translation import Translation
from wordbook.domain import models as domain

__all__ = ('Repo', )


class Repo(base.DbRepo):
    def get_matching_translations(self, language, word_fragment):
        """Get translations matching given language and fragment of the word.

        :param language: ISO639-2 language code; ie. en for English
        :param word_fragment: String

        :returns: List of translations
        :rtype: []domain.Translation
        """
        query = self.session.query(Word).join(Translation).filter_by(
            language=language
        ).filter(
            Word.word.ilike('%{}%'.format(word_fragment))
        ).order_by(Word.word, Translation.translation)

        for translation in query.all():
            print(translation)
            yield domain.Translation(
                from_language=language,
                to_language='',
                word=translation.word,
                translated=translation.word
            )

    def _get_or_create_word(self, language, word, ipa):
        query = self.session.query(Word).filter_by(
            language=language,
            word=word)

        try:
            word = query.one()
        except NoResultFound:
            word = Word(
                language=language,
                word=word,
                ipa=ipa)

            self.session.add(word)
            self.session.commit()

        return word

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
            translation.ipa)

        translation = self._get_or_create_translation(
            word,
            translation.to_language,
            translation.translated)

        return translation
