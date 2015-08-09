import pytest
from sqlalchemy.exc import IntegrityError
from wordbook.infra.db import get_session
from wordbook.infra.models.cardlist import CardAssignment
from wordbook.infra.models.cardlist import List
from wordbook.infra.models.card import Card
from wordbook.infra.models.word import Word


def test_list_and_assignment_creation_and_uniqueness():
    """Test if CardAssignment can be correctly created."""
    session = get_session()
    word = Word(language='en', word='barn', ipa='baarn', simplified='barn')
    session.add(word)
    session.flush()

    card = Card(
        word_id=word.id,
        language='pl',
        translation='Stodoła',
        picture='barn.png',
        definition='Wooden building.'
    )
    session.add(card)
    session.flush()

    li = List(
        name='test1',
        foreign_language='en',
        known_language='pl',
        definitions=True,
        pictorials=True,
    )
    session.add(li)
    session.flush()

    ca = CardAssignment(list_id=li.id, card_id=card.id)
    session.add(ca)
    session.flush()

    ca = CardAssignment(list_id=li.id, card_id=card.id)
    session.add(ca)
    # Test unique for card_id and list_id fields
    with pytest.raises(IntegrityError):
        session.flush()

    session.rollback()
