from app.api import QuestionResource, EChartResource, QuestionnaireResource, CorrectScores, CorrectScoresRank
from app.utils import ExtendedAPI

api = ExtendedAPI()

api.add_resource(QuestionResource, '/questionnaire', endpoint='question')
api.add_resource(EChartResource, '/questionnaire/<string:questionnaire_id>/result', endpoint='result')
api.add_resource(QuestionnaireResource, '/questionnaire/add', endpoint='questionnaire')
# Correct Score
api.add_resource(CorrectScores, '/jcrace/<int:race_id>', endpoint='correct_scores')
api.add_resource(CorrectScoresRank, '/jcrace/<int:race_id>/ranking', endpoint='ranking')


def init_api(app):
    api.init_app(app)
