from flask import Flask


def create_app(config_object):
    app = Flask(__name__)
    # app.config.frompyfile(filename)
    # app.config.from_object(config_object)
    app.config.update(dict(DEBUG=True, SECRET_KEY='houvUgag)'))

    from . import ajax_views
    from . import manage_views
    from . import views

    app.register_blueprint(ajax_views.ajax)
    app.register_blueprint(manage_views.manage)
    app.register_blueprint(views.frontend)

    return app

app = create_app(dict(DEBUG=True, SECRET_KEY='houvUgag)'))
