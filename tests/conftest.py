import sys
import os
import pytest
from alembic.command import upgrade, downgrade
from alembic.config import Config

# TODO: It shouldn't be there.
sys.path.insert(0, os.path.abspath('.'))


TESTDB = 'test_wordbook.db'
TESTDB_PATH = "{}".format(TESTDB)


@pytest.fixture(autouse=True)
def db(request, monkeypatch):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    from wordbook.infra import config
    from wordbook.infra import db

    monkeypatch.setattr(config, 'SQLALCHEMY_ENGINE', 'sqlite:///' + TESTDB_PATH)

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    _engine = create_engine(
        'sqlite:///' + TESTDB_PATH,
        echo=config.SQLALCHEMY_ECHO,
        echo_pool=config.SQLALCHEMY_ECHO_POOL)
    db_session = sessionmaker(bind=_engine)

    def get_session():
        return db_session()

    monkeypatch.setattr(db, 'get_session', get_session)

    alembic_config = Config('alembic.ini')
    alembic_config.set_section_option('alembic', 'sqlalchemy.url', 'sqlite:///' + TESTDB_PATH)

    def teardown():
        downgrade(alembic_config, '18554c40c9e')
        # os.unlink(TESTDB_PATH)

    upgrade(alembic_config, 'head')
    request.addfinalizer(teardown)
    return
