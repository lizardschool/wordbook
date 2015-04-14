from wordbook.infra import db

__all__ = ('DbRepo', )


class DbRepo(object):
    def __init__(self, session=None):
        """Repository initialization.

        :param session: SQLAlchemy session class. If none is given, then default from db module will be used.
        """
        if session is None:
            self.session = db.get_session()
        else:
            self.session = session
