"""Shortcut for importing models.

But real case for this is a necessity of preloading models.
Without that models are not propageted into Model.metadata,
which is used by Alembic during autogeneration process.
"""
from .db import Model   # NOQA
from .models.word import Word   # NOQA
from .models.card import Card     # NOQA
from .models.wordlist import List   # NOQA
from .models.wordlist import CardAssignment   # NOQA
