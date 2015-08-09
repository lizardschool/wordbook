"""Cards repository module."""
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from . import base
from wordbook.infra.models.cardlist import List
from wordbook.domain import models as domain

__all__ = ('CardlistRepo', )


class CardlistRepo(base.DbRepo):

    """List repository."""

    def _row_to_domain_object(self, row):
        """Converts database row into domain object."""
        return domain.List(
            id=row.id,
            name=row.name,
            foreign_language=row.foreign_language,
            known_language=row.known_language,
            definitions=row.definitions,
            pictorials=row.pictorials,
        )

    def all(self):
        """Return all lists."""
        query = self.session.query(List)
        for row in query.all():
            yield self._row_to_domain_object(row)

    def get(self, list_id):
        """Get the list by the id."""
        query = self.session.query(List).filter_by(id=list_id)
        row = query.one()
        return self._row_to_domain_object(row)

    def create(self, name, foreign_language, known_language=None, definitions=False, pictorials=False):
        """Create a new list with a given name."""
        row = List(
            name=name,
            foreign_language=foreign_language,
            known_language=known_language,
            definitions=definitions,
            pictorials=pictorials
            )
        self.session.add(row)
        self.session.commit()
        return self._row_to_domain_object(row)

    # TODO(multilang):
    def add_card(self, card):
        """Add the card.

        A card has a reference to the list, so passing a list id as another
        parameter is not necessary.
        """
        from wordbook.infra.models.cardlist import Card     # TODO(fail)

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

    # TODO(multilang):
    def get_cards_from_list(self, list_id):
        """Return cards from the list.

        Cards are sorted in a descending order by the date of creation.
        """
        from wordbook.infra.models.cardlist import Card     # TODO(fail)

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
                simplified=tr.word.simplified,
                translated=tr.translation
            )
