from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from datetime import timedelta
from app.models.user_model import UserModel
from app.serializers.user_serializer import UserSchema
from app.models.anime_model import AnimeModel
from app.models.users_animes_model import UserAnimeModel
from http import HTTPStatus
import ipdb
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

bp = Blueprint("bp_user", __name__, url_prefix="/users")


@bp.route("/signup/", methods=["POST"])
def create_user():
    session = current_app.db.session

    body = request.get_json()
    username = body.get("username")
    email = body.get("email")
    password = body.get("password")

    user_existence = UserModel.query.filter_by(email=email).first()

    if user_existence != None:
        return {"msg": "User already exists!"}, HTTPStatus.UNPROCESSABLE_ENTITY

    new_user = UserModel(username=username, email=email)
    new_user.password = password

    user_schema = UserSchema()

    session.add(new_user)
    session.commit()

    return user_schema.dump(new_user), HTTPStatus.CREATED


@bp.route("/login/", methods=["POST"])
def login_user():
    session = current_app.db.session

    body = request.get_json()
    email = body.get("email")
    password = body.get("password")

    user = UserModel.query.filter_by(email=email).first()

    user_schema = UserSchema()

    if user == None:
        return {"msg": "Email or password invalid!"}, HTTPStatus.NOT_FOUND

    pass_is_valid = user.check_password(password)

    if pass_is_valid:
        acess_token = create_access_token(
            identity=user.id, expires_delta=timedelta(days=7)
        )
        fresh_token = create_access_token(
            identity=user.id, fresh=True, expires_delta=timedelta(days=30)
        )

        return {"acess_token": acess_token, "fresh_token": fresh_token}, HTTPStatus.OK

    return {"msg": "Email or password invalid!"}, HTTPStatus.NOT_ACCEPTABLE


@bp.route("/add_anime/", methods=["POST"])
@jwt_required()
def add_anime_for_user():
    user_id = get_jwt_identity()
    session = current_app.db.session

    anime_id = request.get_json().get("anime_id")

    verify_if_anime_exists = AnimeModel.query.filter_by(id=anime_id).first()

    if verify_if_anime_exists == None:
        return {"msg": "Anime doesn't exists"}, HTTPStatus.NOT_FOUND

    user_schema = UserSchema()
    user = UserModel.query.filter_by(id=user_id).first()
    verify_if_user_already_has_anime = anime_id in [
        user.get("id") for user in user_schema.dump(user).get("anime_list")
    ]

    if verify_if_user_already_has_anime:
        return {"msg": "User already has anime registered"}, HTTPStatus.NOT_ACCEPTABLE

    add_anime = UserAnimeModel(user_id=user_id, anime_id=anime_id)
    session.add(add_anime)
    session.commit()

    user = UserModel.query.filter_by(id=user_id).first()
    anime_user_schema = user_schema.dump(user).get("anime_list")

    return user_schema.dump(user)


@bp.route("/remove_anime/", methods=["DELETE"])
@jwt_required()
def delete_anime_from_user():
    user_id = get_jwt_identity()
    session = current_app.db.session

    anime_id = request.get_json().get("anime_id")

    verify_if_anime_exists = AnimeModel.query.filter_by(id=anime_id).first()

    if verify_if_anime_exists == None:
        return {"msg": "Anime doesn't exists"}, HTTPStatus.NOT_FOUND

    user_schema = UserSchema()
    user = UserModel.query.filter_by(id=user_id).first()
    verify_if_user_already_has_anime = anime_id in [
        user.get("id") for user in user_schema.dump(user).get("anime_list")
    ]

    if not verify_if_user_already_has_anime:
        return {"msg": "User doesn't has anime registered"}, HTTPStatus.NOT_ACCEPTABLE

    delete_anime = UserAnimeModel.query.filter_by(
        user_id=user_id, anime_id=anime_id
    ).first()
    session.delete(delete_anime)
    session.commit()

    user = UserModel.query.filter_by(id=user_id).first()
    anime_user_schema = user_schema.dump(user).get("anime_list")

    return user_schema.dump(user)


@bp.route("/refresh/")
@jwt_required(fresh=True)
def refresh():
    user_id = get_jwt_identity()
    acess_token = create_refresh_token(
        identity=user_id, expires_delta=timedelta(days=7)
    )

    return {"acess_token": acess_token}