from app.models.user_model import UserModel
from app.models.anime_model import AnimeModel
from app.serializers.anime_serializer import AnimeSchema
from . import ma


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    anime_list = ma.Nested(
        AnimeSchema(
            only=(
                "id",
                "anime_name",
                "author",
            )
        ),
        many=True,
    )
