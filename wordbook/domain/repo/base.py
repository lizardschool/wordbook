from wordbook.infra import db

__all__ = ('DbRepo', )


class DbRepo(object):
    def __init__(self, session=None):
        """Repository initialization.

        :param session: SQLAlchemy session class. If none is given, then default from db module will be used.
        """
        if session is None:
            self.session = db.Session()
        else:
            self.session = session
