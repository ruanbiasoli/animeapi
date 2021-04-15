from flask import Blueprint, request, current_app, jsonify
from ..models.anime_model import AnimeModel
from ..serializers.anime_serializer import AnimeSchema
from http import HTTPStatus

bp = Blueprint("bp_anime", __name__, url_prefix="/animes")


@bp.route("/", methods=["POST"])
def create_anime():
    session = current_app.db.session

    body = request.get_json()
    anime_name = body.get("anime_name")
    author = body.get("author")

    anime_already_exists = AnimeModel.query.filter_by(anime_name=anime_name).first()

    if anime_already_exists != None:
        return {"msg": "Anime already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY

    new_anime = AnimeModel(anime_name=anime_name, author=author)

    anime_schema = AnimeSchema()

    session.add(new_anime)
    session.commit()
    return anime_schema.dump(new_anime), HTTPStatus.CREATED


@bp.route("/")
def list_all_animes():
    list_of_animes = AnimeModel.query.all()
    anime_schema = AnimeSchema()

    return jsonify(list(anime_schema.dump(list_of_animes, many=True)))


@bp.route("/<int:anime_id>/")
def list_anime_by_id(anime_id):
    anime = AnimeModel.query.filter_by(id=anime_id).first()

    if anime == None:
        return {"msg": "not found"}, HTTPStatus.NOT_FOUND

    anime_schema = AnimeSchema()

    return anime_schema.dump(anime), HTTPStatus.OK


@bp.route("/<int:anime_id>/", methods=["DELETE"])
def delete_anime(anime_id):
    session = current_app.db.session

    anime_already_exists = AnimeModel.query.filter_by(id=anime_id).first()

    if anime_already_exists == None:
        return {"msg": "Anime doesn't exists"}, HTTPStatus.NOT_FOUND

    anime = AnimeModel.query.filter_by(id=anime_id).first()

    anime_schema = AnimeSchema()

    session.delete(anime)
    session.commit()
    return {"msg": "Anime sucefully deleted"}, HTTPStatus.NO_CONTENT