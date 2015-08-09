"""Database models for user's list and cards on that list."""
import pycountry
from sqlalchemy import event
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UnicodeText
from sqlalchemy import false
from sqlalchemy import UniqueConstraint
from sqlalchemy import func
from sqlalchemy.orm import relationship
from wordbook.infra import config
from wordbook.infra import db


class List(db.TimestampMixin, db.Model):

    """Model of the list containing selected words."""

    # Fields
    # id
    # created_at
    # modified_at
    name = Column(UnicodeText, nullable=False, index=True)
    foreign_language = Column(Enum(*config.TRANSLATION_LANGUAGES),
                              doc='ISO639-2 language code.',
                              nullable=False)
    known_language = Column(Enum(*config.TRANSLATION_LANGUAGES),
                            doc='ISO639-2 language code.')
    definitions = Column(
        Boolean,
        doc='List can contain cards with definitions in foreign language.',
        default=False,
        server_default=false()
    )
    pictorials = Column(
        Boolean,
        doc='List can contain cards with pictures instead of translated words.',
        default=False,
        server_default=false()
    )
    last_visited_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now())

    # Relationships
    assigned_cards = relationship('CardAssignment', cascade='all, delete-orphan')


class CardAssignment(db.TimestampMixin, db.Model):

    """Model representing assignment of the card to the list."""

    card_id = Column(Integer, ForeignKey('card.id'), nullable=False, index=True)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=False, index=True)

    last_accessed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)

    __table_args__ = (
        UniqueConstraint('card_id', 'list_id', name='_card_list_uc'),
    )


    # TODO(last_access): manager powinien miec metode touch, ktora zmienia date w tym polu, ale nie zapisuje


@event.listens_for(List, 'before_insert')
@event.listens_for(List, 'before_update')
def card_validation(mapper, connection, li):
    """List data validation.

    :raises ValueError: if model is missing some data
    """
    if not (li.known_language or li.definitions or li.pictorials):
        raise ValueError('List must contains known language, pictorials or definitions.')
