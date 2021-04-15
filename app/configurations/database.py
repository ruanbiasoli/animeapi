from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from .serializers import ma

db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.user_model import UserModel
    from app.models.anime_model import AnimeModel
    from app.models.episode_model import EpisodeModel
    from app.models.users_animes_model import UserAnimeModel