from flask_restful import Api

from app.api import QuestionResource, EChartResource

api = Api()

api.add_resource(QuestionResource, '/questionnaire/<string:questionnaire_id>', endpoint='question')
api.add_resource(EChartResource, '/questionnaire/<string:questionnaire_id>/result', endpoint='result')


def init_api(app):
    api.init_app(app)
