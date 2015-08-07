"""Database model for single words."""
import pycountry
from sqlalchemy import Column
from sqlalchemy import UnicodeText
from sqlalchemy.orm import relationship

from wordbook.infra import db

__all__ = ('Word', )


class Word(db.TimestampMixin, db.LanguageMixin, db.Model):

    """Model containing basic informations about the single word."""

    word = Column(UnicodeText, nullable=False)
    ipa = Column(UnicodeText)
    simplified_pronunciation = Column(UnicodeText)

    translations = relationship("Translation", backref='word',
                                cascade="all, delete-orphan")

    def __repr__(self):
        """Text representation."""
        return '<Word(language={language_name}, word={word}, ipa={ipa} simplified={simplified})>'.format(
            language_name=self.language_name,
            word=self.word,
            ipa=self.ipa,
            simplified=self.simplified_pronunciation
        )

    @property
    def language_name(self):
        """Full language name."""
        return pycountry.languages.get(alpha=self.language).name
