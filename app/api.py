import time

from flask import request
from flask_restful import Resource

from app.models import Questionnaire, QuestionnaireData
from app.utils import AuthToken, CommonResponse, WTOKEN
from ext_app import db


class QuestionResource(Resource):
    @AuthToken()
    def get(self, questionnaire_id, user_id):
        print(user_id)
        # print(request.values.get("b"))
        questionnaire = Questionnaire.query.filter(Questionnaire.id == questionnaire_id,
                                                   Questionnaire.is_delete == 0).first()
        if not questionnaire:
            return CommonResponse(404, False, "Questionnaire not found", {})()
        data = vars(questionnaire)
        # print(data)
        data.update(questions=[])
        questions = questionnaire.questions
        for question in questions:
            question_data = vars(question)
            question_data.update(answers=[])
            data.get("questions").append(question_data)
            answers = question.answers
            for answer in answers:
                answer_data = vars(answer)
                answer_data.pop('_sa_instance_state')
                question_data.get("answers").append(answer_data)
            question_data.pop('_sa_instance_state')
        data.pop('_sa_instance_state')
        questionnaire_data = QuestionnaireData.query.filter(QuestionnaireData.user_id == user_id,
                                                            QuestionnaireData.questionnaire_id == questionnaire_id).first()
        has_participated = 0
        if questionnaire_data:
            has_participated = 1
        data.update(has_participated=has_participated)
        return CommonResponse(200, True, "", data)()

    @AuthToken()
    def post(self, questionnaire_id, user_id):
        """
        [{
                question_id:1,
                answer_id:1,
                answer:"548645658",
                questionnaire_id:1,
        }]
        :param questionnaire_id:
        :param user_id:
        :return:
        """
        content_type = request.headers.get("Content-Type")
        if "son" not in content_type:
            return CommonResponse(404, False, "Incorrect Content-Type", {})()
        questionnaire = Questionnaire.query.filter(Questionnaire.id == questionnaire_id,
                                                   Questionnaire.is_delete == 0).first()
        if not questionnaire:
            return CommonResponse(404, False, "Questionnaire not found", {})()
        # 过期时间问题
        if questionnaire.end_at < time.time():
            return CommonResponse(404, False, "Questionnaire Expired", {})()

        questionnaire_data = QuestionnaireData.query.filter(QuestionnaireData.user_id == user_id,
                                                            QuestionnaireData.questionnaire_id == questionnaire_id).first()
        if questionnaire_data:
            return CommonResponse(404, False, "Incorrect Content-Type", {})()

        res_data = request.json
        print(res_data)
        item_list = []
        for res_datum in res_data:
            questionnaire_data = QuestionnaireData(
                question_id=res_datum.get("question_id"),
                answer_id=res_datum.get("answer_id"),
                answer=res_datum.get("answer"),
                questionnaire_id=questionnaire_id,
                user_id=user_id,
            )
            item_list.append(questionnaire_data)
        db.session.bulk_save_objects(item_list)
        db.session.commit()
        db.session.close()
        return CommonResponse(200, True, "ok", {})()


class QuestionnaireResource(Resource):
    def post(self):
        """
        {
         "create_at": 14514545,
         "end_at": 14514545,
        "description": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "title": "问卷1",
        "start_at": 14514545,
        " questions": [
         {
                "number": 1,
                "answer_type": 1,
                "question": "wenti 1",
                "required": 1,
                "answers": [
                    {
                        "answer": "1231",
                        "number": 1,
                        "question_id": 1
                    },
                    {
                        "answer": "21311",
                        "number": 2,
                        "question_id": 1
                    }
                ]
            },
        }
        :return:
        """
        content_type = request.headers.get("Content-Type")
        w_token = request.headers.get("WToken")
        if w_token != WTOKEN:
            return CommonResponse(401, False, "Insufficient permissions", {})()
        if "son" not in content_type:
            return CommonResponse(404, False, "Incorrect Content-Type", {})()
        res_data = request.json
        item_list = []
        questionnaire = Questionnaire(

        )

    def put(self):
        content_type = request.headers.get("Content-Type")
        w_token = request.headers.get("WToken")
        if w_token != WTOKEN:
            return CommonResponse(401, False, "Insufficient permissions", {})()
        if "son" not in content_type:
            return CommonResponse(404, False, "Incorrect Content-Type", {})()
        res_data = request.json

    def delete(self):
        content_type = request.headers.get("Content-Type")
        w_token = request.headers.get("WToken")
        if w_token != WTOKEN:
            return CommonResponse(401, False, "Insufficient permissions", {})()
        if "son" not in content_type:
            return CommonResponse(404, False, "Incorrect Content-Type", {})()
        res_data = request.json


class EChartResource(Resource):
    def get(self, questionnaire_id):
        questionnaire = Questionnaire.query.filter(Questionnaire.id == questionnaire_id).first()
        if not questionnaire:
            return CommonResponse(404, False, "Questionnaire not found", {})()
        data = vars(questionnaire)
        data.update(questions=[])
        questions = questionnaire.questions
        for question in questions:
            question_data = vars(question)
            question_data.update(answers=[])
            data.get("questions").append(question_data)
            answers = question.answers
            answer_datas = question.answer_data
            if question.answer_type == 3:
                for answer_data in answer_datas:
                    answer_datum = {"name": answer_data.answer, "value": 1}
                    question_data.get("answers").append(answer_datum)
            else:
                for answer in answers:
                    answer_datum = {"name": answer.answer, "value": answer.data.count()}
                    question_data.get("answers").append(answer_datum)
            question_data.pop('_sa_instance_state')
        data.pop('_sa_instance_state')
        return CommonResponse(200, True, "", data)()
