from flask.app import Flask
from .user_view import bp as bp_user
from .anime_view import bp as bp_anime
from .episode_view import bp as bp_episode

def init_app(app: Flask):
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_anime)
    app.register_blueprint(bp_episode)