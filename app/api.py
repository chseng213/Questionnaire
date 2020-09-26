import json
import time

from flask import request
from flask_restful import Resource
from sqlalchemy import desc

from app.models import Questionnaire, QuestionnaireData, QuestionnaireQuestion, QuestionnaireAnswer, JCRace, Races, \
    JCTicket, Accounts, JCCorrectScore, Orders, PointTrace, JCRanking, UserProfile, League, Team
from app.utils import AuthToken, CommonJsonRet, WTOKEN, OSS_URL, CommonRequestParser, get_order_code
from ext_app import db


class QuestionResource(Resource):
    @AuthToken()
    def get(self, user_id):
        # print(request.values.get("b"))
        questionnaire = Questionnaire.query.filter(
            Questionnaire.is_delete == 0).order_by(desc(Questionnaire.id)).first()
        if not questionnaire:
            return CommonJsonRet(404, False, "Questionnaire not found", {})()
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
                                                            QuestionnaireData.questionnaire_id == questionnaire.id).first()
        has_participated = 0
        if questionnaire_data:
            has_participated = 1
        data.update(has_participated=has_participated)
        return CommonJsonRet(200, True, "", data)()

    @AuthToken()
    def post(self, user_id):
        """
        [{
                question_id:1,
                answer_id:1,
                answer:"548645658",
                questionnaire_id:1,
        }]
        :param user_id:
        :return:
        """
        content_type = request.headers.get("Content-Type")
        if "son" not in content_type:
            return CommonJsonRet(400, False, "Incorrect Content-Type", {})()
        questionnaire = Questionnaire.query.filter(
            Questionnaire.is_delete == 0).order_by(desc(Questionnaire.id)).first()
        if not questionnaire:
            return CommonJsonRet(404, False, "Questionnaire not found", {})()
        # 过期时间问题
        if questionnaire.end_at < time.time():
            return CommonJsonRet(404, False, "Questionnaire Expired", {})()
        questionnaire_data = QuestionnaireData.query.filter(QuestionnaireData.user_id == user_id,
                                                            QuestionnaireData.questionnaire_id == questionnaire.id).first()
        if questionnaire_data:
            return CommonJsonRet(400, False, "User Has Been Participated ", {})()

        res_data = request.json
        print(res_data)
        item_list = []
        for res_datum in res_data:
            if isinstance(res_datum.get("answer_id"), list):
                if res_datum.get("answer_id"):
                    for answer_id in set(res_datum.get("answer_id")):
                        questionnaire_data = QuestionnaireData(
                            question_id=res_datum.get("question_id"),
                            answer_id=answer_id,
                            answer=res_datum.get("answer") if res_datum.get("answer") else "",
                            questionnaire_id=questionnaire.id,
                            user_id=user_id,
                        )
                        item_list.append(questionnaire_data)
                else:
                    questionnaire_data = QuestionnaireData(
                        question_id=res_datum.get("question_id"),
                        answer_id=-1,
                        answer=res_datum.get("answer") if res_datum.get("answer") else "",
                        questionnaire_id=questionnaire.id,
                        user_id=user_id,
                    )
                    item_list.append(questionnaire_data)
            elif isinstance(res_datum.get("answer_id"), int):
                questionnaire_data = QuestionnaireData(
                    question_id=res_datum.get("question_id"),
                    answer_id=res_datum.get("answer_id"),
                    answer=res_datum.get("answer") if res_datum.get("answer") else "",
                    questionnaire_id=questionnaire.id,
                    user_id=user_id,
                )
                item_list.append(questionnaire_data)
            else:
                return CommonJsonRet(400, False, "Error answer_id type", {})()
        account = Accounts.query.filter(Accounts.user_id == user_id).first()
        cat = int(time.time())
        account.available = account.available + 50000
        order_num = get_order_code()
        order_desc = f"Questionnaire points"

        pt = PointTrace(
            user_id=user_id,
            create_at=cat,
            points=50000,
            desc=order_desc,
            title=order_desc,
            way=order_desc,
            order_num=order_num,
            current=account.available,
        )
        item_list.append(pt)
        order = Orders(
            user_id=user_id,
            order_num=order_num,
            create_at=cat,
            pay_time=cat,
            number=50000,
            source="Questionnaire points",
            desc=order_desc,
        )
        item_list.append(order)

        db.session.bulk_save_objects(item_list)
        db.session.commit()
        db.session.close()
        return CommonJsonRet(200, True, "success", {})()


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
            return CommonJsonRet(401, False, "Insufficient permissions", {})()
        if "son" not in content_type:
            return CommonJsonRet(404, False, "Incorrect Content-Type", {})()
        res_data = request.json

        questionnaire = Questionnaire(
            title=res_data.get("title"),
            description=res_data.get("description"),
            create_at=res_data.get("create_at"),
            end_at=res_data.get("end_at"),
            start_at=res_data.get("start_at")
        )
        db.session.add(questionnaire)
        db.session.commit()
        questions = res_data.get("questions")
        for i, question in enumerate(questions, 1):
            question_obj = QuestionnaireQuestion(
                questionnaire_id=questionnaire.id,
                number=i,
                question=question.get("question"),
                answer_type=question.get("answer_type"),
                required=question.get("required")
            )
            db.session.add(question_obj)
            db.session.commit()
            question_id = question_obj.id
            answers = question.get("answers")
            if answers:
                answer_list = []
                for j, answer in enumerate(answers, 1):
                    answer_obj = QuestionnaireAnswer(
                        question_id=question_id,
                        number=j,
                        answer=answer.get("answer")
                    )
                    answer_list.append(answer_obj)
                db.session.bulk_save_objects(answer_list)
                db.session.commit()

        return CommonJsonRet(200, True, "", {})()

    def put(self):
        content_type = request.headers.get("Content-Type")
        w_token = request.headers.get("WToken")
        if w_token != WTOKEN:
            return CommonJsonRet(401, False, "Insufficient permissions", {})()
        if "son" not in content_type:
            return CommonJsonRet(404, False, "Incorrect Content-Type", {})()
        res_data = request.json

    def delete(self):
        content_type = request.headers.get("Content-Type")
        w_token = request.headers.get("WToken")
        if w_token != WTOKEN:
            return CommonJsonRet(401, False, "Insufficient permissions", {})()
        if "son" not in content_type:
            return CommonJsonRet(404, False, "Incorrect Content-Type", {})()
        res_data = request.json


class EChartResource(Resource):
    def get(self, questionnaire_id):
        questionnaire = Questionnaire.query.filter(Questionnaire.id == questionnaire_id).first()
        if not questionnaire:
            return CommonJsonRet(404, False, "Questionnaire not found", {})()
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
                    if answer_data.answer:
                        answer_datum = {"name": answer_data.answer, "value": 1}
                        question_data.get("answers").append(answer_datum)
            else:
                for answer in answers:
                    answer_datum = {"name": answer.answer, "value": answer.data.count()}
                    question_data.get("answers").append(answer_datum)
            question_data.pop('_sa_instance_state')
        data.pop('_sa_instance_state')
        total = QuestionnaireData.query.filter(QuestionnaireData.questionnaire_id == questionnaire_id).group_by(
            QuestionnaireData.user_id).count()
        data.update(total=total)
        return CommonJsonRet(200, True, "", data)()


class CorrectScores(Resource):
    @AuthToken()
    def get(self, race_id, user_id):
        """
        判断比赛是否被选中
        :param race_id:
        :param user_id:
        :return:
        """
        race = Races.query.filter(Races.race_id == race_id).first()
        if not race:
            return CommonJsonRet(400, False, "Invalid race_id", {})()
        league = League.query.filter(League.league_id == race.league_id).first()
        home = Team.query.filter(Team.team_id == race.home_id).first()
        guest = Team.query.filter(Team.team_id == race.guest_id).first()
        data = {
            "race": {
                "race_id": race.race_id,
                "race_time": race.race_time,
                "league": league.en_name,
                "home": home.en_name,
                "home_logo": OSS_URL.format(home.betradar_id),
                "guest": guest.en_name,
                "guest_logo": OSS_URL.format(guest.betradar_id),
                "scores": "VS" if not race.scores else "-".join(json.loads(race.scores)),
            },
            "correct_scores": {
                "1": [],
                "X": [],
                "2": [],
            },
            "user_record": {

            }}
        user_record = JCTicket.query.filter(JCTicket.uid == user_id, JCTicket.rid == race_id).first()
        able_to_bet = 1
        has_participated = 0
        if user_record:
            has_participated = 1
            able_to_bet = 0
            ranking = db.session.execute(
                """
select ranking 
from (SELECT
        t.*,
        @rownum := @rownum + 1 AS ranking 
    FROM
        ( SELECT id, user_id,username,vote, avatar,title,pay_num, settle_num 
            FROM `activity`.jc_ranking 
            where race_id=:race_id  
            ORDER BY settle_num desc,pay_num desc,id) t ,
        ( SELECT @rownum := 0 ) r ) rr 
	where rr.user_id=:user_id """,
                {
                    "race_id": race_id,
                    "user_id": user_id
                }).fetchone()
            data.get("user_record").update(
                {
                    "vote": user_record.vote,
                    "settle_number": user_record.settle_number if user_record.settle_number else int(
                        user_record.odds * user_record.number),
                    "result": user_record.result,

                    "ranking": int(ranking[0]),
                }
            )
        if race.is_delete == 1 or race.is_started != 3:
            able_to_bet = 0
        odds = JCRace.query.filter(JCRace.race_id == race.race_id).first()._odds
        for odd in odds:
            header = odd.header
            data.get("correct_scores").get(header).append(
                {
                    "name": odd.name,
                    "odds": odd.odds,
                    "sort": odd.sort,
                }
            )
        data.get("correct_scores").get("1").sort(key=lambda x: x.get("sort"))
        data.get("correct_scores").get("2").sort(key=lambda x: x.get("sort"))
        data.get("correct_scores").get("X").sort(key=lambda x: x.get("sort"))
        data.update(has_participated=has_participated)
        data.update(able_to_bet=able_to_bet)
        return CommonJsonRet(200, True, "success", data)()

    @AuthToken()
    def post(self, race_id, user_id):
        """
        提交用户下注方案
        :param race_id:
        :param user_id:
        :return:
        """
        # 参数定义
        parse = CommonRequestParser()
        parse.add_argument('vote', type=str, location='form', required=True)
        parse.add_argument('odds', type=str, location='form', required=True)
        parse.add_argument('number', type=int, location='form', required=True)
        args = parse.parse_args()
        vote = args.get("vote", "")
        print(vote)
        odds = args.get("odds", "")
        cat = int(time.time())
        number = args.get("number", 0)
        # 判断限额
        if not 100 <= number <= 100000:
            return CommonJsonRet(400, False, "Point must between 100 and 100000", {})()
        query_start = time.time()
        # 判断用户是否已参加
        jc_ticket_ = JCTicket.query.filter(JCTicket.rid == race_id, JCTicket.uid == user_id).first()
        if jc_ticket_:
            return CommonJsonRet(400, False, "You has been participated", {})()
        # 判断比赛
        race = Races.query.filter(Races.race_id == race_id).first()
        league = League.query.filter(League.league_id == race.league_id).first().en_name
        home = Team.query.filter(Team.team_id == race.home_id).first().en_name
        guest = Team.query.filter(Team.team_id == race.guest_id).first().en_name
        print(f"query race  {time.time()-query_start}")
        if not race:
            return CommonJsonRet(400, False, "Invalid race_id", {})()
        if race.is_delete == 1:
            return CommonJsonRet(400, False, "Match Postponed ", {})()
        if race.is_started != 3:
            return CommonJsonRet(400, False, "Match has started ", {})()
        # 判断积分
        account = Accounts.query.filter(Accounts.user_id == user_id).first()
        user = UserProfile.query.filter(UserProfile.id == user_id).first()
        if account.available < number:
            return CommonJsonRet(301, True, "Insufficient points,please redeem", {})()
        correct_score = JCCorrectScore.query.filter(JCCorrectScore.race_id == race_id,
                                                    JCCorrectScore.name == vote).first()
        query_end = time.time()
        if not correct_score:
            return CommonJsonRet(400, False, "Invalid vote", {})()
        # 生成下注记录,订单记录,积分记录,更新用户积分
        account.available = account.available - number
        jc_ticket = JCTicket(
            uid=user_id,
            rid=race_id,
            cat=cat,
            number=number,
            vote=vote,
            league=league,
            home=home,
            guest=guest,
            odds=odds if correct_score.odds == odds else correct_score.odds,
        )
        order_num = get_order_code()
        order_desc = f"{league} {home} {guest} {vote}"
        order = Orders(
            user_id=user_id,
            order_num=order_num,
            create_at=cat,
            pay_time=cat,
            number=number,
            desc=order_desc,
        )
        pt = PointTrace(
            user_id=user_id,
            create_at=cat,
            points=0 - number,
            desc=order_desc,
            order_num=order_num,
            current=account.available,
        )
        jc_rank = JCRanking(
            user_id=user_id,
            race_id=race_id,
            pay_num=number,
            username=user.username,
            vote=vote,
            avatar=user.avatar,
            title=f"{home} VS {guest}",
        )
        item_list = [account, jc_ticket, order, pt, jc_rank]
        db.session.bulk_save_objects(item_list)
        db.session.commit()
        print(f"query time : {query_start-query_end},commit time :{time.time()-query_end}")
        db.session.close()
        return CommonJsonRet(200, True, "success", {})()


class CorrectScoresRank(Resource):
    @AuthToken()
    def get(self, race_id, user_id):
        jc_race = JCRace.query.filter(JCRace.race_id == race_id, JCRace.selected == 1).first()
        if not jc_race:
            return CommonJsonRet(400, False, "Invalid race_id", {})()
        data = {
            "user_rank": {},
            "ranking": [],
            "current_title": {},
            "all_title": [],
            "is_over": jc_race.settled
        }
        user_record = JCTicket.query.filter(JCTicket.uid == user_id, JCTicket.rid == race_id).first()
        if user_record:
            data.update(
                user_rank={
                    "vote": user_record.vote,
                    "settle_number": user_record.settle_number if user_record.settle_number else int(
                        user_record.odds * user_record.number),
                    "result": user_record.result,
                }
            )
        rankings = db.session.execute(
            """
            SELECT
                t.*,
                @rownum := @rownum + 1 AS ranking 
            FROM
                ( SELECT id, user_id,username,vote, avatar,title,pay_num, settle_num 
                    FROM `activity`.jc_ranking 
                    where race_id=:race_id  ORDER BY settle_num desc,pay_num desc,id) t ,
                ( SELECT @rownum := 0 ) r
            """,
            {"race_id": race_id}
        ).fetchall()
        if rankings:
            data.get("current_title").update({
                "title": rankings[0][5],
                "race_id": race_id
            })
            for ranking in rankings:
                data.get("ranking").append(
                    {
                        "ranking": int(ranking[-1]),
                        "avatar": ranking[4],
                        "username": ranking[2],
                        "vote": ranking[3],
                        "pay_number": ranking[-3],
                        "settle_number": ranking[-2],
                    }
                )
                if ranking.user_id == user_id:
                    data.get("user_rank").update(ranking=int(ranking[-1]))
        else:
            # 当前title 以及历史积分榜title
            race = Races.query.filter(Races.race_id == race_id).first()
            home = Team.query.filter(Team.team_id == race.home_id).first()
            guest = Team.query.filter(Team.team_id == race.guest_id).first()
            data.get("current_title").update({
                "title": " ".join([home.en_name, "VS", guest.en_name]),
                "race_id": race_id
            })
        # all_title
        all_title = JCRanking.query.filter(JCRanking.race_id != race_id).group_by(JCRanking.title).all()
        if all_title:
            for title in all_title:
                data.get("all_title").append(
                    {
                        "title": title.title,
                        "race_id": title.race_id
                    }

                )
        return CommonJsonRet(200, True, "success", data)()
