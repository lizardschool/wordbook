"""Database model for single words."""
import pycountry
from sqlalchemy import Column
from sqlalchemy import UnicodeText
from sqlalchemy.orm import relationship

from wordbook.infra import db

__all__ = ('Word', )


class Word(db.TimestampMixin, db.LanguageMixin, db.Model):
    """Model containing basic informations about single word."""
    word = Column(UnicodeText, nullable=False)
    ipa = Column(UnicodeText)

    translations = relationship("Translation", backref='word',
                                cascade="all, delete-orphan")

    def __repr__(self):
        return '<Word(language={language_name}, word={word}, ipa={ipa})>'.format(
            language_name=self.language_name,
            word=self.word,
            ipa=self.ipa
        )

    @property
    def language_name(self):
        return ''
        return pycountry.languages.get(alpha=self.language).name
