import pytest
from wordbook.infra.db import get_session
from wordbook.infra.models.card import Card
from wordbook.infra.models.word import Word


def test_card_creation():
    """Test if card can be created correctly."""
    session = get_session()
    word = Word(language='en', word='barn', ipa='baarn', simplified='barn')
    session.add(word)
    session.commit()

    card = Card(
        word_id=word.id,
        language='pl',
        translation='Stodoła',
        picture='barn.png',
        definition='Wooden building.'
    )
    session.add(card)
    session.commit()

    db_card = session.query(Card).filter_by(id=card.id).one()

    assert db_card.id == card.id
    assert db_card.word_id == word.id
    assert db_card.language == 'pl'
    assert db_card.translation == 'Stodoła'
    assert db_card.picture == 'barn.png'
    assert db_card.definition == 'Wooden building.'
    assert db_card.created_at is not None
    assert db_card.modified_at is not None


def test_card_translation_validation():
    """Card should have translation with language."""
    session = get_session()
    word = Word(language='en', word='cat', ipa='kat', simplified='kat')
    session.add(word)
    session.flush()

    card = Card(
        word_id=word.id,
        language='en',
        translation='',
    )
    session.add(card)
    with pytest.raises(ValueError):
        session.flush()
    session.rollback()


def test_card_translation_without_language_validation():
    """Card should have translation with language."""
    session = get_session()
    word = Word(language='en', word='cat', ipa='kat', simplified='kat')
    session.add(word)
    session.flush()

    card = Card(
        word_id=word.id,
        language='',
        translation='Stodoła',
    )
    session.add(card)
    with pytest.raises(ValueError):
        session.flush()
    session.rollback()


def test_card_without_anything_validation():
    """Card should have translation, picture or definition."""
    session = get_session()
    word = Word(language='en', word='cat', ipa='kat', simplified='kat')
    session.add(word)
    session.flush()

    card = Card(
        word_id=word.id,
    )
    session.add(card)
    with pytest.raises(ValueError):
        session.flush()
    session.rollback()


def test_card_with_picture_validation():
    """Card should validate with picture."""
    session = get_session()
    word = Word(language='en', word='cat', ipa='kat', simplified='kat')
    session.add(word)
    session.flush()

    card = Card(
        word_id=word.id,
        picture='cat.png',
    )
    session.add(card)
    session.flush()
    session.rollback()


def test_card_with_definition_validation():
    """Card should validate with definition."""
    session = get_session()
    word = Word(language='en', word='cat', ipa='kat', simplified='kat')
    session.add(word)
    session.flush()

    card = Card(
        word_id=word.id,
        definition='Furry little animal.',
    )
    session.add(card)
    session.flush()
    session.rollback()
