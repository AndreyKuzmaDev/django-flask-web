from datetime import timedelta

from flask import Flask, request, jsonify
from flask_jwt_simple import JWTManager

from tools.misc import make_resp, check_keys, create_jwt_generate_response
from users.repo import InMemoryUsersRepo

app = Flask(__name__)
app.user_repo = InMemoryUsersRepo()
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRES'] = timedelta(hours=24)
app.config['JWT_IDENTITY_CLAIM'] = 'user'
app.config['JWT_HEADER_NAME'] = 'authorization'
app.jwt = JWTManager(app)
app.user_repo.request_create('user', '12345678')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/api/register', methods=['POST'])
def user_register():
    in_json = request.json
    if not in_json:
        return make_resp(jsonify({'message': 'Empty request'}), 400)
    elif not check_keys(in_json, ('username', 'password')):
        return make_resp(jsonify({'message': 'Bad request'}), 400)
    created_user = app.user_repo.request_create(**in_json)
    if created_user is None:
        return make_resp(jsonify({'message': 'Duplicated user'}), 400)
    return create_jwt_generate_response(created_user)


@app.route('/api/login', methods=['POST'])
def user_login():
    in_json = request.json
    if not in_json:
        return make_resp(jsonify({'message': 'Empty request'}), 400)
    elif not check_keys(in_json, ('username', 'password')):
        return make_resp(jsonify({'message': 'Bad request'}), 400)
    user, error = app.user_repo.authorize(**in_json)
    if user is None:
        return make_resp(jsonify({'message': error}), 400)
    return create_jwt_generate_response(user)


if __name__ == '__main__':
    app.run()
