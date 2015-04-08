from . import base
from wordbook.infra.models.wordlist import List
from wordbook.infra.models.wordlist import Card

__all__ = ('Repo', )


class Repo(base.DbRepo):
    def foo(self):
        pass
