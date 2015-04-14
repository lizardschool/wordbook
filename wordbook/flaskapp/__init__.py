from flask import Flask

app = Flask(__name__)
# app.config.frompyfile(filename)
app.config.update(
    DEBUG=True,
    SECRET_KEY='houvUgag)'
)

from . import ajax_views    # NOQA
from . import manage_views  # NOQA
from . import views         # NOQA
