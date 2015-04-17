from flask import url_for


def test_add_translation(app, client):
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
