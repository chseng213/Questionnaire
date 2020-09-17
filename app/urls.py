from flask_restful import Api

from app.api import QuestionResource, EChartResource, QuestionnaireResource

api = Api()

api.add_resource(QuestionResource, '/questionnaire', endpoint='question')
api.add_resource(EChartResource, '/questionnaire/<string:questionnaire_id>/result', endpoint='result')
api.add_resource(QuestionnaireResource, '/questionnaire/add', endpoint='questionnaire')


def init_api(app):
    api.init_app(app)
