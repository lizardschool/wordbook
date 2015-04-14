"""Database initialization module.

Useful documentation
--------------------

* SQLAlchemy column types: http://docs.sqlalchemy.org/en/rel_0_9/core/type_basics.html
* Common Filter Operators: http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#common-filter-operators
* All column operators:
  http://docs.sqlalchemy.org/en/rel_0_9/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators

"""
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from . import config

__all__ = ('Model', 'TimestampMixin', 'LanguageMixin', 'get_session')


# http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#sqlalchemy.create_engine
def get_session():
    engine = create_engine(config.SQLALCHEMY_ENGINE, echo=config.SQLALCHEMY_ECHO, echo_pool=config.SQLALCHEMY_ECHO_POOL)
    Session = sessionmaker(bind=engine)
    return Session()


class Base(object):
    id = Column(Integer, primary_key=True)

    # __table_args__ = {'mysql_engine': 'InnoDB'}
    # __mapper_args__= {'always_refresh': True}

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

# http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base
#: Base class for declarative class definitions.
Model = declarative_base(cls=Base)


class TimestampMixin(object):
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    modified_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.current_timestamp())


class LanguageMixin(object):
    language = Column(Enum(*config.TRANSLATION_LANGUAGES),
                      doc='ISO639-2 language code.',
                      nullable=False)
