#__*__ encoding:utf-8 __*__
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///music.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
class Music(db.Model):
    __tablename__="Music"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    singer_name=db.Column(db.String(20),nullable=False)
    song_name=db.Column(db.String(20),nullable=False)
    album_name=db.Column(db.String(20),nullable=False)
    irics=db.Column(db.Text,nullable=False)
db.create_all()
