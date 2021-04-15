from app.models import db


class UserAnimeModel(db.Model):
    __tablename__ = "users_animes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    anime_id = db.Column(
        db.Integer, db.ForeignKey("animes.id", onupdate="CASCADE", ondelete="CASCADE")
    )
