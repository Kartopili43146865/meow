from extensions import db, app

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    img = db.Column(db.String)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()