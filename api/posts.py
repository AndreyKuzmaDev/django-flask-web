from flask import jsonify
from flask_restful import Resource

from app.app import main_app


class PostListRes(Resource):
    def get(self):
        return jsonify(main_app.post_repo.get_all())