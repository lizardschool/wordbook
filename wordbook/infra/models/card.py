"""Database model for single card."""

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UnicodeText
from sqlalchemy import event
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


@event.listens_for(Card, 'before_insert', once=True)
@event.listens_for(Card, 'before_update', once=True)
def card_validation(mapper, connection, card):
    """Card data validation.

    :raises ValueError: if model is missing some data
    """
    translation = (card.translation and card.language)
    picture = card.picture
    definition = card.definition

    if not (picture or definition or translation):
        raise ValueError('Card must contain translation (with language), picture or definition.')

    if (card.translation or card.language) and not translation:
        raise ValueError('Language and translation are required.')
