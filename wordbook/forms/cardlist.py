"""Forms to operate on list of cards."""
import pycountry
from flask_wtf import Form
from wtforms import StringField
from wtforms import SelectField
from wtforms import validators
from wordbook.infra import config


def languages_choices():
    """Language choices for use in form."""
    choices = []
    for iso_code in config.TRANSLATION_LANGUAGES:
        choices.append((iso_code, pycountry.languages.get(alpha2=iso_code).name))

    return list(sorted(choices, key=lambda t: t[1]))


class CardlistForm(Form):

    """List creation form."""

    name = StringField(
        'Name',
        validators=[validators.Length(min=4, max=35), validators.DataRequired()],
        description='Name of the list.'
    )
    foreign_language = SelectField(
        'Foreign language',
        choices=languages_choices(),
        validators=[validators.required()],
        description='Select language which the student is learning.'
    )
    known_language = SelectField(
        'Known language',
        choices=languages_choices(),
        validators=[validators.required()],
        description='Select language which is already known by the student. Native language is prefered.',
        default='pl',
    )

    def validate_known_language(form, field):
        """Validate known language.

        It cannot be equal to foreign language.
        For ie. English-English lists there will be the `definitions` field.
        """
        if form.data['foreign_language'] == field.data:
            raise validators.ValidationError('Known language cannot be the same as foreign language.')
        return field
