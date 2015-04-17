from wordbook.domain.models import List


def test_list_hash():
    li = List(id=1, name='abc')
    assert li.hash == 'eLrzL'

    li.id = 2
    assert li.hash == 'oLEWq'
