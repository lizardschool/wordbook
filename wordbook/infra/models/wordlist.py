"""Database models for user's list and cards on that list."""
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UnicodeText
from sqlalchemy.orm import relationship
from wordbook.infra import db


class List(db.TimestampMixin, db.Model):
    name = Column(UnicodeText, nullable=False)
    cards = relationship('Card', cascade='all, delete-orphan')
    # TODO: foreign language
    # TODO: known language


class Card(db.TimestampMixin, db.Model):
    translation_id = Column(Integer, ForeignKey('translation.id'), nullable=False)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=False)

    translation = relationship('Translation', backref='cards')
