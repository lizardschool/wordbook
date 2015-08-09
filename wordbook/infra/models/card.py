"""Database model for single card."""

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UnicodeText
from wordbook.infra import db
from wordbook.infra import config

__all__ = ('Card', )


class Card(db.TimestampMixin, db.Model):

    """Model representing single card with translation, definition or picture."""

    word_id = Column(Integer, ForeignKey('word.id'), nullable=False, index=True)

    language = Column(Enum(*config.TRANSLATION_LANGUAGES),
                      doc='ISO639-2 language code.')
    translation = Column(UnicodeText)

    picture = Column(UnicodeText)

    definition = Column(UnicodeText)
