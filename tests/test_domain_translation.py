from wordbook.domain.models import Translation


def test_translation_dto():
    t = Translation(
        id=1,
        from_language='en',
        into_language='pl',
        word='apple',
        ipa='ejpyl',
        simplified='epyl',
        translated='jabłko',
    )
    assert t.dto_autocomplete() == dict(
        id=1,
        word='apple',
        translation='jabłko',
        ipa='ejpyl',
        simplified='epyl',
    )
