from database import db

class Blocklist(db.Model):
    __tablename__ = 'blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
