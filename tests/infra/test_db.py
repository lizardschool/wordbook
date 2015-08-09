from wordbook.infra.db import get_session
from wordbook.domain.repo.cardlist import CardlistRepo


def test_single_session(db_session):
    """Session should be singleton.

    It should be the same session in every context.
    """

    session1 = get_session()
    session2 = get_session()

    assert id(db_session) == id(session1)
    assert id(session1) == id(session2)
    assert id(CardlistRepo().session) == id(session1)
