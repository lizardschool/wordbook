""""""
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UnicodeText
from sqlalchemy.orm import relationship
from wordbook.infra import db


class List(db.TimestampMixin, db.Model):
    name = Column(UnicodeText, nullable=False)
    cards = relationship('Card', cascade='all, delete-orphan')


class Card(db.TimestampMixin, db.Model):
    translation = Column(Integer, ForeignKey('translation.id'), nullable=False)
    list = Column(Integer, ForeignKey('list.id'), nullable=False)
