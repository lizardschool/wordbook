"""Database model for single words."""
import pycountry
from sqlalchemy import Column
from sqlalchemy import UnicodeText
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from wordbook.infra import db

__all__ = ('Word', )


class Word(db.TimestampMixin, db.LanguageMixin, db.Model):

    """Model containing basic informations about the single word."""

    word = Column(UnicodeText, nullable=False)
    ipa = Column(UnicodeText)
    simplified = Column(UnicodeText)

    cards = relationship(
        "Card",
        backref='card',
        cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('word', 'language', name='_word_language_uc'),
    )

    def __repr__(self):
        """Verbose representation."""
        return '<Word(language={language_name}, word={word}, ipa={ipa}, simplified={simplified})>'.format(
            language_name=self.language_name,
            word=self.word,
            ipa=self.ipa,
            simplified=self.simplified
        )

    @property
    def language_name(self):
        """Full language name."""
        return pycountry.languages.get(alpha2=self.language).name
