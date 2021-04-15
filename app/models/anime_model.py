from app.models import db
from app.models.user_model import UserModel
from .users_animes_model import UserAnimeModel


class AnimeModel(db.Model):
    __tablename__ = "animes"

    id = db.Column(db.Integer, primary_key=True)
    anime_name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=True)

    users_list = db.relationship(
        "UserModel", backref="anime_list", secondary="users_animes"
    )
