from flask import redirect
from flask import url_for
from flask import render_template
from . import app
from wordbook.domain.repo.cardlist import CardlistRepo
from wordbook.forms.cardlist import CardlistForm


@app.route('/manage')
def manage():
    return render_template('manage.html')


@app.route('/manage/show-lists/', defaults={'page': 1})
@app.route('/manage/show-lists/<int:page>')
def show_lists(page):
    # TODO: add pagination
    lists = CardlistRepo().all()
    return render_template(
        'show_lists.html',
        lists=lists
    )


@app.route('/manage/create-list', methods=['GET', 'POST'])
def create_list():
    form = CardlistForm()
    if form.validate_on_submit():
        cardlist = CardlistRepo().create(form.name.data)
        return redirect(url_for('edit_list', list_id=cardlist.id))
    return render_template('create_list.html', form=form)


@app.route('/manage/edit-list/<int:list_id>')
def edit_list(list_id):
    # Get matching translation should accept list id
    # to exclude words which already exists on it
    # translations = TranslationRepo()
    language = 'en'
    cardlist = CardlistRepo().get(list_id)

    return render_template(
        'edit_list.html',
        language=language,
        cardlist=cardlist
    )
