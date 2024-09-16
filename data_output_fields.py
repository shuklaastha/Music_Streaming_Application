from flask_restful import fields

song_fields={
    "id": fields.Integer,
    "name":fields.String,
    "lyrics":fields.String
}

user_fields={
    "id": fields.Integer,
    "name":fields.String,
    "email":fields.String,
    # "password":fields.String
}

