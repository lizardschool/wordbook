from wordbook.domain.repo.translation import Repo
from wordbook.domain.models import Translation


def test_add_translation():
    repo = Repo()
    translation = repo.add_translation(
        Translation(from_language='en', into_language='pl', word='Apple', ipa='epyl', translated='Jabłko')
    )
    assert translation.id is not None

    dbtr = repo.get(translation.id)
    assert dbtr.id == translation.id
    assert dbtr.from_language == translation.from_language
    assert dbtr.into_language == translation.into_language
    assert dbtr.word == translation.word
    assert dbtr.ipa == translation.ipa
    assert dbtr.translated == translation.translated


def test_get_matching_translations():
    repo = Repo()
    repo.add_translation(
        Translation(from_language='en', into_language='pl', word='Ship', ipa='szip', translated='Statek')
    )
    repo.add_translation(
        Translation(from_language='en', into_language='pl', word='Apple', ipa='epyl', translated='Jabłko')
    )

    matching = list(repo.get_matching_translations(1, 'ap'))
    assert len(matching) == 1
    tr = matching[0]
    assert isinstance(tr, Translation)
    assert tr.word == 'Apple'
    assert tr.ipa == 'epyl'
    assert tr.translated == 'Jabłko'
    assert tr.from_language == 'en'
    assert tr.into_language == 'pl'
