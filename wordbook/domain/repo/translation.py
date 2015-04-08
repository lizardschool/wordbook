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

    def add_translation(self, translation):
        assert isinstance(translation, domain.Translation)
        query = self.session.query(Word).filter_by(
            language=translation.from_language,
            word=translation.word)

        try:
            word = query.one()
        except NoResultFound:
            word = Word(
                language=translation.from_language,
                word=translation.word,
                ipa=translation.ipa)
            self.session.add(word)
            self.session.commit()

        # trans_query = self.session.query(Translation)


