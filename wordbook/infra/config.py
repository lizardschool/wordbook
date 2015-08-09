"""Module with configuration constants."""

####################
#
# i18n/l10n
#
####################

LOCALE = 'pl'
TRANSLATION_LANGUAGES = ('en', 'pl', 'fr', 'es', )

####################
#
# Database
#
####################

# http://docs.sqlalchemy.org/en/rel_0_9/dialects/sqlite.html
# http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#sqlalchemy.create_engine
# http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#database-urls
# Change it also in alembic.ini
#: Path to a DB Engine
SQLALCHEMY_ENGINE = 'sqlite:///wordbook.db'
# SQLALCHEMY_ENGINE = 'sqlite:///:memory:'

#: Is produced SQLs should be logged (bool|str)
#: If set to the string "debug",
#: result rows will be printed to the standard output as well.
SQLALCHEMY_ECHO = False
SQLALCHEMY_ECHO_POOL = SQLALCHEMY_ECHO
