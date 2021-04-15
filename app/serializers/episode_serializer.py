from app.models.episode_model import EpisodeModel
from app.models.user_model import UserModel
from app.models.anime_model import AnimeModel
from . import ma


class EpisodeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EpisodeModel

    id = ma.auto_field()
    episode_name = ma.auto_field()
    anime_id = ma.auto_field()
