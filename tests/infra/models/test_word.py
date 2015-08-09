import pytest
from sqlalchemy.exc import IntegrityError
from wordbook.infra.models.word import Word
from wordbook.infra.db import get_session


def test_word_repr():
    """Test word's repr()."""
    word = Word(language='en', word='ship', ipa='szyp', simplified='szip')
    expected = '<Word(language=English, word=ship, ipa=szyp, simplified=szip)>'
    assert repr(word) == expected


def test_word_language_name():
    """Test language_name property."""
    word = Word(language='en', word='ship', ipa='szyp', simplified='szip')
    assert word.language_name == 'English'


def test_word_uniqueness():
    """Test if unique is working."""
    session = get_session()

    word = Word(
        language='en',
        word='ship',
        ipa='szyp',
        simplified='szip')

    session.add(word)
    session.commit()

    word = Word(
        language='en',
        word='ship',
        ipa='szyp',
        simplified='szip')
    session.add(word)

    with pytest.raises(IntegrityError):
        session.commit()
