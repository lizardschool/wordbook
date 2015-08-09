from flask import redirect
from flask import url_for
from flask import render_template
from flask import Blueprint
from wordbook.domain.repo.cardlist import CardlistRepo
from wordbook.forms.cardlist import CardlistForm

manage = Blueprint('manage', __name__, url_prefix='/manage')


@manage.route('/')
def index():
    """Entry point for management.

    .. http:get:: /manage/
    """
    return render_template('manage.html')


@manage.route('/show-lists')
def show_lists():
    """Show all defined lists.

    .. http:get:: /manage/show-lists
    """
    lists = CardlistRepo().all()
    return render_template(
        'show_lists.html',
        lists=lists
    )


@manage.route('/create-list', methods=['GET', 'POST'])
def create_list():
    """Create new list view.

    .. http:get:: /manage/create-list

    .. http:post:: /manage/create-list

      :query name: List name
      :query foreign_language: Foreign language
      :query known_language: Language already known by the student
    """
    form = CardlistForm()
    if form.validate_on_submit():
        cardlist = CardlistRepo().create(
            form.name.data,
            form.foreign_language.data,
            form.known_language.data
        )
        return redirect(url_for('manage.edit_list', list_id=cardlist.id))
    return render_template('create_list.html', form=form)


@manage.route('/edit-list/<int:list_id>')
def edit_list(list_id):
    # Get matching translation should accept list id
    # to exclude words which already exists on it
    # translations = TranslationRepo()
    cardlist = CardlistRepo().get(list_id)

    return render_template(
        'edit_list.html',
        cardlist=cardlist
    )
