from flask import Flask
from os import getenv
from config import config_selector


def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    from .views import init_app
    from .configurations import (
        database,
        commands,
        authentication,
        migrations,
        serializers,
    )

    config_type = config_selector[getenv("FLASK_ENV")]
    app.config.from_object(config_type)

    database.init_app(app)
    migrations.init_app(app)
    commands.init_app(app)
    views.init_app(app)
    database.ma.init_app(app)
    authentication.init_app(app)
    serializers.init_app(app)

    return app