from flask import url_for
from wordbook.domain.repo.translation import Repo


def test_add_translation(app, client):
    """Test of add_translation ajax view.

    Translation should be added to repository and returned in response.
    """
    data = dict(
        word='sheep',
        ipa='sziip',
        translation='owca',
        from_language='en',
        into_language='pl',
    )
    resp = app.test_client().post(
        url_for('ajax.add_translation'),
        data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert resp.status_code == 200
    assert resp.json == dict(translation=dict(id=1, ipa='sziip', translation='owca', word='sheep'))

    repo = Repo()
    translation = repo.get(resp.json['translation']['id'])
    assert translation.translated == 'owca'
    assert translation.from_language == 'en'
    assert translation.word == 'sheep'
    assert translation.ipa == 'sziip'
    assert translation.into_language == 'pl'
