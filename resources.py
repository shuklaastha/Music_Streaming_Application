from flask_restful import Resource, Api, marshal_with, request
from model import *
from parserr import *
from data_output_fields import *
from flask import request


api=Api(prefix='/api')

class song_api(Resource):

    @marshal_with(song_fields)
    def get(self):
        print('hey')
        return Song.query.all()
    
    def post(self):
        id = request.get_json().get('id')
        name = request.get_json().get('name')
        lyrics = request.get_json().get('lyrics')
        
        song_data = Song(
            id=id,
            name=name,
            lyrics=lyrics,
        )
        # args=song_parser.parse_args()
        # song_data=Song(**args)

        db.session.add(song_data)
        db.session.commit()
        return {"message":"Song added successfully!"}

api.add_resource(song_api,'/song_data')





class user_api(Resource):

    @marshal_with(user_fields)
    def get(self):
        return User.query.all()
    
    def post(self):
        # id = request.get_json().get('id')
        # name = request.get_json().get('name')
        # email = request.get_json().get('email')
        # password = request.get_json().get('password')
        
        # user_data = User(
        #     id=id,
        #     name=name,
        #     email=email,
        #     password=password,
        # )
        args=user_parser.parse_args()
        user_data=User(**args)

        
        db.session.add(user_data)
        db.session.commit()
        return {"message":"User added successfully!"}

api.add_resource(user_api,'/user_data')




