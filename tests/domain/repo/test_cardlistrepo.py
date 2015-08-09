import pytest
from sqlalchemy.exc import IntegrityError
from wordbook.domain import models as domain
from wordbook.infra.models.cardlist import List
from wordbook.domain.repo.cardlist import CardlistRepo


def test_get_all_cardlists(db_session):
    """Test returning of all lists."""
    li1 = List(
        name='test1',
        foreign_language='en',
        known_language='pl',
        definitions=True,
        pictorials=True,
    )
    li2 = List(
        name='test2',
        foreign_language='fr',
        known_language='pl',
        definitions=True,
        pictorials=True,
    )

    db_session.add(li1)
    db_session.add(li2)

    lists = list(CardlistRepo().all())
    assert len(lists) == 2
    assert all([isinstance(li, domain.List) for li in lists])
    assert lists[0].id == li1.id
    assert lists[1].id == li2.id
    assert lists[0].name == li1.name
    assert lists[1].name == li2.name

    assert lists[1].foreign_language == 'fr'
    assert lists[1].known_language == 'pl'
    assert lists[1].definitions is True
    assert lists[1].pictorials is True


def test_get_cardlist_by_id(db_session):
    """Test getting a card list by the specified id."""
    li1 = List(
        name='test1',
        foreign_language='en',
        known_language='pl',
        definitions=True,
        pictorials=True,
    )
    li2 = List(
        name='test2',
        foreign_language='en',
        known_language='pl',
        definitions=True,
        pictorials=True,
    )

    db_session.add(li1)
    db_session.add(li2)
    db_session.flush()  # We need id's

    assert li1.id != li2.id

    repo = CardlistRepo()
    db_li1 = repo.get(li1.id)
    db_li2 = repo.get(li2.id)

    assert db_li1.id == li1.id
    assert db_li1.name == 'test1'
    assert isinstance(db_li1, domain.List)
    assert db_li1.foreign_language == 'en'
    assert db_li1.known_language == 'pl'
    assert db_li1.definitions is True
    assert db_li1.pictorials is True

    assert db_li2.id == li2.id
    assert db_li2.name == 'test2'
    assert isinstance(db_li2, domain.List)


def test_create_cardlist(db_session):
    """Test new cardlist creation via repository."""
    repo = CardlistRepo()
    lists = list(repo.all())
    assert len(lists) == 0

    # Validation - known_language, definitions or pictorials
    with pytest.raises(ValueError):
        repo.create('test1', 'en')
    db_session.rollback()

    # Unknown language code
    with pytest.raises(IntegrityError):
        repo.create('test', 'jp', 'pl')
    db_session.rollback()

    cardlist = repo.create('test1', 'en', 'pl')
    assert isinstance(cardlist, domain.List)
    assert cardlist.name == 'test1'
    assert cardlist.foreign_language == 'en'
    assert cardlist.known_language == 'pl'
    assert cardlist.definitions is False
    assert cardlist.pictorials is False

    cardlist = repo.create('test2', 'en', None, True, False)
    assert isinstance(cardlist, domain.List)
    assert cardlist.name == 'test2'
    assert cardlist.foreign_language == 'en'
    assert cardlist.known_language is None
    assert cardlist.definitions is True
    assert cardlist.pictorials is False

    cardlist = repo.create('test3', 'en', None, False, True)
    assert isinstance(cardlist, domain.List)
    assert cardlist.name == 'test3'
    assert cardlist.foreign_language == 'en'
    assert cardlist.known_language is None
    assert cardlist.definitions is False
    assert cardlist.pictorials is True
