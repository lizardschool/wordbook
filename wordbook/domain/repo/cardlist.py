from sqlalchemy.orm.exc import NoResultFound
from . import base
from wordbook.infra.models.wordlist import List
from wordbook.infra.models.wordlist import Card
from wordbook.domain import models as domain

__all__ = ('CardlistRepo', )


class CardlistRepo(base.DbRepo):
    def all(self, page=1):
        # TODO: respect page numer
        query = self.session.query(List)
        for row in query.all():
            yield domain.List(
                id=row.id,
                name=row.name
            )

    def get(self, list_id):
        query = self.session.query(List).filter_by(id=list_id)
        row = query.one()
        return domain.List(id=row.id, name=row.name)

    def create(self, name):
        cardlist = List(name=name)
        self.session.add(cardlist)
        self.session.commit()
        return domain.List(id=cardlist.id, name=cardlist.name)

    def add_card(self, card):
        list_query = self.session.query(List).filter_by(id=card.list_id)
        cardlist = list_query.one()
        # TODO: if list does not exists then it should throw an exception

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

    def get_translations(self, list_id, limit=10, offset=0):
        card_query = self.session.query(Card).filter_by(list_id=list_id).limit(limit).offset(offset)
        # TODO: single query (join with translation and with word)
        for row in card_query.all():
            tr = row.translation
            yield domain.Translation(
                from_language=tr.word.language,
                info_language=tr.language,
                word=tr.word.word,
                ipa=tr.word.word,
                translated=tr.translation
            )
