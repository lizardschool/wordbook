import pycountry
from wordbook.infra import config


def test_translation_languages_values():
    """Translation languages should be correct ISO codes."""
    for iso_code in config.TRANSLATION_LANGUAGES:
        pycountry.languages.get(alpha2=iso_code)


def test_translation_languages_uniqueness():
    """Translation languages should be unique."""
    unique = list(sorted(set(config.TRANSLATION_LANGUAGES)))
    assert list(sorted(config.TRANSLATION_LANGUAGES)) == unique
