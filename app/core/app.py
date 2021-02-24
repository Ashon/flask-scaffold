from logging.config import dictConfig

from flask import Flask

from core.context import api
from core.context import db
from core.context import migrate


def create_app(name, settings, routes):
    app = Flask(name)

    # set logger
    if getattr(settings, 'LOGGING', None):
        dictConfig(settings.LOGGING)

    # log bootstrap appliation
    app.logger.info('Start Application')
    for k, v in settings.__dict__.items():
        # skip builtins
        if k.find('__') > 1 and type(v) in (int, str, list, dict):
            app.logger.info(f'{k} = {v}')

    app.config.from_object(settings)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app, spec_kwargs={
        'info': {
            'description': settings.API_DESCRIPTION
        }
    })
    for route in routes:
        api.register_blueprint(route)

    app.logger.info('Application Initialized')

    return app
