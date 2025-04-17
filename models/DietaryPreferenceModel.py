from db import db

class DietaryPreferenceModel(db.Model):
    __tablename__ = 'DietaryPreference'
    id = db.Column(db.Integer, primary_key=True)
    exclude_cuisine= db.Column(db.String, nullable=True)
    exclude_ingredients=db.Column(db.String, nullable=True)
    max_sugar=db.Column(db.Integer, nullable=False, default=999)
    intolerances=db.Column(db.String, nullable=True)
    diets=db.Column(db.String, nullable=True)

    user_id = db.Column(db.String, db.ForeignKey('User.id'), nullable=False, unique=True)
    user = db.relationship("UserModel", back_populates="dietary_preferences")


