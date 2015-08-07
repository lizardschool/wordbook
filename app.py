#!/usr/bin/env python
import os
import rollbar
from flask import got_request_exception

if __name__ == '__main__':
    from wordbook.flaskapp import dev_app as app
    app.run(debug=True)
else:
    from wordbook.flaskapp import app   # NOQA


@app.before_first_request
def init_rollbar():
    """Initialize rollbar module.

    It also allows person tracking.
    https://github.com/rollbar/rollbar-flask-example/blob/master/hello.py
    """
    rollbar.init(
        '2deae0df9d884836ab6eb7ea3057b992',
        # environment name
        'development',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
