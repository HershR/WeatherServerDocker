import os
from flask import Flask
from .extensions import db, migrate, scheduler


def create_app():

    # create and configure the app
    app = Flask(__name__)

    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)

    """
    Flask Scheduler setup from documentation
    https://github.com/viniciuschiele/flask-apscheduler/blob/master/examples/application_factory/__init__.py
    """

    # pylint: disable=C0415, W0611
    with app.app_context():

        # pylint: disable=W0611
        if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            from . import tasks  # noqa: F401
            scheduler.start()

        from . import weather
        app.register_blueprint(weather.bp)

        from . import cities
        app.register_blueprint(cities.bp)
        app.add_url_rule('/', endpoint='index')

        return app
