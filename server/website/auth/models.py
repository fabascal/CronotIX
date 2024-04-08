from website import db
from uuid import uuid4
from flask import current_app as app
from website.auth.utils.loginUtils import hash_pass
from flask_login import UserMixin

def get_uuid4():
    return uuid4().hex

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False, default=get_uuid4)
    username = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)
    last_login_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    @property
    def plaintext_password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @plaintext_password.setter
    def plaintext_password(self, password):
        self.password = hash_pass(password)


@app.login_manager.user_loader
def login_manager(user_id):
    user = User.query.get(user_id).first()
    try:
        user.last_login_at = db.func.now()
        db.session.commit()
    except:
        pass        
    return User.query.get(user_id)