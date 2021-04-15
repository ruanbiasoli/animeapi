from app.models.anime_model import AnimeModel
from app.models.users_animes_model import UserAnimeModel
from . import ma


class AnimeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AnimeModel

    id = ma.auto_field()
    anime_name = ma.auto_field()
    author = ma.auto_field()
    users_list = ma.auto_field()
