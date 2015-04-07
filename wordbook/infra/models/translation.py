"""Database model for word translation."""
from sqlalchemy import Column
from sqlalchemy import UnicodeText
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from wordbook.infra import db

__all__ = ('Translation', )


class Translation(db.TimestampMixin, db.LanguageMixin, db.Model):
    translation = Column(UnicodeText, nullable=False)
    word_id = Column(Integer, ForeignKey('word.id'))

    word = relationship('Word', backref=backref('translations', order_by=translation))

