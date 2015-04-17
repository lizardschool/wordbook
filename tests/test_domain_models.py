import pytest
from wordbook.domain.models import List


def test_invalid_field_setattr():
    li = List(id=1, name='abc')
    with pytest.raises(AttributeError):
        li.foo = 3

    assert li.id == 1

    li.id = 2
    assert li.id == 2


def test_invalid_field_getattr():
    li = List(id=1, name='bca')
    with pytest.raises(AttributeError):
        li.foo


def test_not_set_field_getattr():
    li = List(id=3)
    assert li.name is None
