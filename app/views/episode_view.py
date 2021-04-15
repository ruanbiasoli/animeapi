from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from app.models.anime_model import AnimeModel
from app.models.episode_model import EpisodeModel
from app.serializers.episode_serializer import EpisodeSchema

bp = Blueprint("bp_episode", __name__, url_prefix="/episodes")


@bp.route("/<int:anime_id>/", methods=["POST"])
def create_episode(anime_id):
    session = current_app.db.session

    anime_exist = AnimeModel.query.filter_by(id=anime_id).first()
    if not anime_exist:
        return {"msg": "Anime doesn't exists"}, HTTPStatus.BAD_REQUEST

    body = request.get_json()
    episode_name = body.get("episode_name")

    episode_already_exist = EpisodeModel.query.filter_by(
        episode_name=episode_name, anime_id=anime_id
    ).first()

    if episode_already_exist != None:
        return {"msg": "This episode already exist"}, HTTPStatus.UNPROCESSABLE_ENTITY

    new_episode = EpisodeModel(episode_name=episode_name, anime_id=anime_id)
    episode_schema = EpisodeSchema()

    session.add(new_episode)
    session.commit()

    return episode_schema.dump(new_episode)


@bp.route("/<int:anime_id>/")
def list_episodes(anime_id):
    verify_if_anime_exist = AnimeModel.query.filter_by(id=anime_id).first()

    if verify_if_anime_exist == None:
        return {"msg": "Not found"}, HTTPStatus.NOT_FOUND

    episode_list = EpisodeModel.query.filter_by(anime_id=anime_id).all()
    episode_schema = EpisodeSchema()

    data = {
        "anime_name": verify_if_anime_exist.anime_name,
        "episode_list": list(episode_schema.dump(episode_list, many=True)),
    }

    return jsonify(data), HTTPStatus.OK
