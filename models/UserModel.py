from db import db

class UserModel(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    # bookmarked recipes
    # mealhistory
    # preferences

