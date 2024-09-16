
from extension import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    creator = db.Column(db.String(10))
    blacklist=db.Column(db.Boolean(), default=False)
    albums = db.relationship('Album', back_populates='user')
    songs = db.relationship('Song', back_populates='user')


class Song(db.Model,UserMixin):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    lyrics = db.Column(db.Text, nullable=False)
    creator_name = db.Column(db.String(80), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    rating= db.Column(db.Float, default=0.0)
    number=db.Column(db.Integer, default=0)
    genre = db.Column(db.String(120), nullable=False)
    flag=db.Column(db.Boolean(), default=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    album = db.relationship('Album', back_populates='songs')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='songs')


class Album(db.Model, UserMixin):
    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    flag=db.Column(db.Boolean(), default=False)
    songs = db.relationship('Song', back_populates='album')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='albums')


class Playlist(db.Model):
    _tablename_ = "playlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    songs = db.relationship('Song', secondary='playlist_songs', backref='playlists')


playlist_songs = db.Table('playlist_songs',
    db.Column('playlist_id', db.String(36), db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('song_id', db.String(36), db.ForeignKey('songs.id'), 
    primary_key=True))





