from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return 'User>>> {self.username}'

    @classmethod
    def generate_userid(cls, **kwargs):
        id = random.randint(100000, 999999)
        while True:
            if cls.query.filter_by(id=id).first():
                id = random.randint(100000, 999999)
            else: break
        return id
    

