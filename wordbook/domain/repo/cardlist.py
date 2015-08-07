"""Cards repository module."""
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from . import base
from wordbook.infra.models.wordlist import List
from wordbook.infra.models.wordlist import Card
from wordbook.domain import models as domain

__all__ = ('CardlistRepo', )


class CardlistRepo(base.DbRepo):

    """Cards repository."""

    def all(self):
        """Return all lists."""
        # TODO: respect page numer
        query = self.session.query(List)
        for row in query.all():
            yield domain.List(
                id=row.id,
                name=row.name
            )

    def get(self, list_id):
        """Get the list by the id."""
        query = self.session.query(List).filter_by(id=list_id)
        row = query.one()
        return domain.List(id=row.id, name=row.name)

    def create(self, name):
        """Create a new list with a given name."""
        # TODO(multilang): it must receive information about both languages.
        cardlist = List(name=name)
        self.session.add(cardlist)
        self.session.commit()
        return domain.List(id=cardlist.id, name=cardlist.name)

    def add_card(self, card):
        """Add the card.

        A card has a reference to the list, so passing a list id as another
        parameter is not necessary.
        """
        list_query = self.session.query(List).filter_by(id=card.list_id)
        cardlist = list_query.one()
        # TODO(errorhandling): if list does not exists then it should throw an exception

        card_query = self.session.query(Card).filter_by(
            list_id=cardlist.id,
            translation_id=card.translation_id)

        try:
            db_card = card_query.one()
        except NoResultFound:
            db_card = Card(
                translation_id=card.translation_id,
                list_id=cardlist.id
            )

            self.session.add(db_card)
            self.session.commit()

        return card

    def get_cards_from_list(self, list_id):
        """Return cards from the list.

        Cards are sorted in a descending order by the date of creation.
        """
        card_query = self.session.query(Card).filter_by(list_id=list_id).order_by(desc('created_at'))
        # TODO(optimization): single query (join with translation and with word)
        for row in card_query.all():
            tr = row.translation
            yield domain.Translation(
                id=tr.id,
                from_language=tr.word.language,
                into_language=tr.language,
                word=tr.word.word,
                ipa=tr.word.ipa,
                simplified=tr.word.simplified_pronunciation,
                translated=tr.translation
            )
