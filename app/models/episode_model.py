from app.models import db


class EpisodeModel(db.Model):
    __tablename__ = "episodes"

    id = db.Column(db.Integer, primary_key=True)
    episode_name = db.Column(db.String, nullable=False)

    anime_id = db.Column(
        db.Integer, db.ForeignKey("animes.id", onupdate="CASCADE", ondelete="CASCADE")
    )
