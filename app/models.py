import time

from ext_app import db


class Questionnaire(db.Model):
    __tablename__ = "questionnaire"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    is_delete = db.Column(db.Integer, nullable=False, default=0)
    create_at = db.Column(db.Integer, default=time.time(), onupdate=time.time)
    start_at = db.Column(db.Integer, nullable=False)
    end_at = db.Column(db.Integer, nullable=False)
    questions = db.relationship("QuestionnaireQuestion", backref='questionnaire', lazy='dynamic')


class QuestionnaireQuestion(db.Model):
    __tablename__ = "questionnaire_question"

    id = db.Column(db.Integer, primary_key=True)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey("questionnaire.id"))
    question = db.Column(db.Text)
    number = db.Column(db.Integer)
    answer_type = db.Column(db.Integer)
    required = db.Column(db.Integer, nullable=False, default=0)
    answers = db.relationship("QuestionnaireAnswer", backref='question', lazy='dynamic')
    answer_data = db.relationship("QuestionnaireData", backref='question_obj', lazy='dynamic')


class QuestionnaireAnswer(db.Model):
    __tablename__ = "questionnaire_answer"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questionnaire_question.id"))
    answer = db.Column(db.Text)
    number = db.Column(db.Integer)
    data = db.relationship("QuestionnaireData", backref='answer_obj', lazy='dynamic')


class QuestionnaireData(db.Model):
    __tablename__ = "questionnaire_data"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    questionnaire_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey("questionnaire_question.id"))
    answer_id = db.Column(db.Integer, db.ForeignKey("questionnaire_answer.id"))
    answer = db.Column(db.Text)


class Races(db.Model):
    """
    赛事表
    """
    __tablename__ = "races"

    race_id = db.Column(db.Integer, primary_key=True)
    race_time = db.Column(db.Integer, nullable=False)
    home_id = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, nullable=False)
    league_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.VARCHAR(5))
    en_status = db.Column(db.VARCHAR(5))
    status_s = db.Column(db.VARCHAR(5), nullable=False)
    half_scores = db.Column(db.VARCHAR(10), nullable=False, default="")
    scores = db.Column(db.VARCHAR(10), nullable=False, default="")
    # focus = db.Column(db.Integer, default=0)
    is_started = db.Column(db.Integer, nullable=False, default=1)
    is_delete = db.Column(db.Integer, nullable=False, default=0)
    cuptree_id = db.Column(db.Integer, nullable=False, default=0)
    update_at = db.Column(db.Integer, default=0, onupdate=time.time)


class Team(db.Model):
    """
    球队表
    """
    __tablename__ = "team"

    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100), nullable=False)
    en_name = db.Column(db.VARCHAR(50), nullable=False)
    standard_name = db.Column(db.VARCHAR(100), nullable=False)
    sb_name = db.Column(db.VARCHAR(100), nullable=False)
    initial = db.Column(db.VARCHAR(1), nullable=False)
    en_initial = db.Column(db.VARCHAR(1), nullable=False)
    country_id = db.Column(db.Integer, nullable=False)
    betradar_id = db.Column(db.VARCHAR(100), default="")
    da_rate = db.Column(db.VARCHAR(5), nullable=False, default="")
    xiao_rate = db.Column(db.VARCHAR(5), nullable=False, default="")
    juesha_rate = db.Column(db.VARCHAR(5), nullable=False, default="")


class League(db.Model):
    """
    联赛表
    """
    __tablename__ = "league"

    league_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100), nullable=False, index=True)
    en_name = db.Column(db.VARCHAR(50), nullable=False, index=True)
    standard_name = db.Column(db.VARCHAR(100), nullable=False, index=True)
    sb_name = db.Column(db.VARCHAR(100), nullable=False)
    short_name = db.Column(db.VARCHAR(50), nullable=False)
    initial = db.Column(db.VARCHAR(1), nullable=False)
    en_initial = db.Column(db.VARCHAR(1), nullable=False)
    country_id = db.Column(db.Integer, index=True)
    is_hot = db.Column(db.Integer, nullable=False, default=0)
    da_rate = db.Column(db.VARCHAR(5), nullable=False, default="")
    xiao_rate = db.Column(db.VARCHAR(5), nullable=False, default="")
    juesha_rate = db.Column(db.VARCHAR(5), nullable=False, default="")


class JCRace(db.Model):
    """
    赛程表
    """
    __tablename__ = "jc_race"

    race_id = db.Column(db.Integer, primary_key=True)
    selected = db.Column(db.Integer, default=0)
    settled = db.Column(db.Integer, default=0)


class JCCorrectScore(db.Model):
    """
    盘口表

    """
    __tablename__ = "jc_correct_score"

    race_id = db.Column(db.Integer, primary_key=True)
    odds = db.Column(db.VARCHAR(200))
    header = db.Column(db.VARCHAR(200))
    name = db.Column(db.VARCHAR(200))


class JCTicket(db.Model):
    """
    下注记录表
    """
    __tablename__ = "jcticket"
    __bind_key__ = "jifen"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    cat = db.Column(db.Integer, default=time.time)
    rid = db.Column(db.Integer)
    number = db.Column(db.Integer)
    status = db.Column(db.Integer, default=1)
    settle_at = db.Column(db.Integer, default=time.time)
    settle_number = db.Column(db.Integer, default=0)
    vote = db.Column(db.VARCHAR(255))
    league = db.Column(db.VARCHAR(255))
    home = db.Column(db.VARCHAR(255))
    guest = db.Column(db.VARCHAR(255))
    scores = db.Column(db.VARCHAR(255))
    result = db.Column(db.VARCHAR(200), default="")
    odds = db.Column(db.DOUBLE)


class Orders(db.Model):
    """
    下注记录表
    """
    __tablename__ = "orders"
    __bind_key__ = "jifen"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    create_at = db.Column(db.Integer)
    pay_time = db.Column(db.Integer)
    number = db.Column(db.Integer)
    isstartpan = db.Column(db.Integer, default=1)
    order_num = db.Column(db.VARCHAR(255))
    source = db.Column(db.VARCHAR(255), default="JC Correct Scores Pick'em")
    desc = db.Column(db.VARCHAR(255))
    type = db.Column(db.Integer, default=30)


class PointTrace(db.Model):
    """
    下注记录表
    """
    __tablename__ = "point_trace"
    __bind_key__ = "jifen"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    create_at = db.Column(db.Integer)
    title = db.Column(db.VARCHAR(255))
    way = db.Column(db.VARCHAR(255))
    point = db.Column(db.Integer)
    status = db.Column(db.Integer, default=1)
    desc = db.Column(db.VARCHAR(255))
    order_num = db.Column(db.VARCHAR(255))
    current = db.Column(db.Integer)


class Accounts(db.Model):
    """
    下注记录表
    """
    __tablename__ = "accounts"
    __bind_key__ = "jifen"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    total = db.Column(db.Integer)
    lockout = db.Column(db.Integer)
    available = db.Column(db.Integer)
    status = db.Column(db.Integer, default=1)
