from extensions import db, app, login_meneger
from flask_login import UserMixin


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    img = db.Column(db.String)
    like = db.Column(db.Integer)
    username = db.Column(db.String)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    password = db.Column(db.String)

@login_meneger.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()