"""Database model for word translation."""
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UnicodeText

from wordbook.infra import db

__all__ = ('Translation', )


class Translation(db.TimestampMixin, db.LanguageMixin, db.Model):
    translation = Column(UnicodeText, nullable=False)
    word_id = Column(Integer, ForeignKey('word.id'))

    # word = relationship('Word', backref=backref('_translations', order_by=translation))
