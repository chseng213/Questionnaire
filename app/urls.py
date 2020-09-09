from flask_restful import Api

from app.api import QuestionResource

api = Api()

api.add_resource(QuestionResource, '/questionnaire/<string:questionnaire_id>', endpoint='question')


def init_api(app):
    api.init_app(app)
