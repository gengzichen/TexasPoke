from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    coin = db.Column(db.Integer)
    password = db.Column(db.String(128))
    
    def set_password(self,password):
        self.password = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password,password)

    def __init__(self, username, password, coin):
        self.username = username
        self.set_password(password)
        self.coin = coin

    def user_info(self):
        username=self.username
        coin = self.coin

        return [username,coin]
