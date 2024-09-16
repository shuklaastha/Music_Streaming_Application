from flask_restful import reqparse


# class Song(db.Model,UserMixin):
#     __tablename__ = "songs"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     lyrics = db.Column(db.Text, nullable=False)
#     creator_name = db.Column(db.String(80), nullable=False)
#     creation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     rating= db.Column(db.Float, default=0.0)
#     number=db.Column(db.Integer, default=0)
#     genre = db.Column(db.String(120), nullable=False)
#     flag=db.Column(db.Boolean(), default=False)
#     album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
#     album = db.relationship('Album', back_populates='songs')
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', back_populates='songs')

song_parser=reqparse.RequestParser()
song_parser.add_argument('id',type=int,help='id missing', required=True)
song_parser.add_argument('name',type=str,help='name missing', required=True)
song_parser.add_argument('lyrics',type=str,help='lyrics missing', required=True)

user_parser=reqparse.RequestParser()
user_parser.add_argument('id',type=int,help='id missing', required=True)
user_parser.add_argument('name',type=str,help='name missing', required=True)
user_parser.add_argument('email',type=str,help='email missing', required=True)
user_parser.add_argument('password',type=str,help='password missing', required=True)
