from db import db

class UserModel(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    # bookmarked recipes
    # mealhistory
    # preferences

