from datetime import timedelta

from flask import Flask, request, jsonify
from flask_jwt_simple import JWTManager

from tools.misc import make_resp, check_keys, create_jwt_generate_response
from users.repo import InMemoryUsersRepo
from users.sqlite_repo import SqliteUsersRepo

app = Flask(__name__)
app.json_encoder = MyJSONEncoder
app.user_repo = SqliteUsersRepo('./db/redditclone.db')
# app.user_repo = InMemoryUsersRepo()
app.posts_repo = InMemoryPostsRepo()
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRES'] = timedelta(hours=24)
app.config['JWT_IDENTITY_CLAIM'] = 'user'
app.config['JWT_HEADER_NAME'] = 'authorization'
# app.user_repo.request_create('user', '12345678')
app.jwt = JWTManager(app)


if __name__ == '__main__':
    app.run()
