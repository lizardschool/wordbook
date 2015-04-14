import sys
import os
import pytest
from alembic.command import upgrade, downgrade
from alembic.config import Config
from wordbook.infra import config


# TODO: It shouldn't be there.
sys.path.insert(0, os.path.abspath('.'))


TESTDB = 'test_wordbook.db'
TESTDB_PATH = "{}".format(TESTDB)


@pytest.fixture(scope='session')
def db(request, monkeypatch):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    monkeypatch.setattr(config, 'SQLALCHEMY_ENGINE', 'sqlite:///' + TESTDB_PATH)

    alembic_config = Config('alembic.ini')

    def teardown():
        downgrade(alembic_config, '18554c40c9e')
        # os.unlink(TESTDB_PATH)

    upgrade(alembic_config, 'head')
    request.addfinalizer(teardown)
    return
