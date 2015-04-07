from wordbook.infra import db
from wordbook.infra.models.word import Word
from wordbook.infra.models.translation import Translation


class Repo(object):
    def __init__(self, session=None):
        """Repository initialization.

        :param session: SQLAlchemy session class. If none is given, then default from db module will be used.
        """
        if session is None:
            self.session = db.Session()
        else:
            self.session = session

    def get_matching(self, language, word_fragment):
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
        translations = query.all()
        # TODO: convert into domain objects
        return translations
