from wordbook.domain.models import List


def test_list_hash():
    li = List(id=1, name='abc')
    assert li.hash == 'eLrzL'

    li.id = 2
    assert li.hash == 'oLEWq'


def test_cardlist_foreign_language_name():
    """Test returning cardlist foreign language iso code to name."""
    li = List(
        name='test1',
        foreign_language='de',
        known_language='pl',
        definitions=True,
        pictorials=True,
    )
    assert li.foreign_language_name == 'German'
