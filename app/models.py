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
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer, db.ForeignKey("questionnaire_answer.id"))
    answer = db.Column(db.Text)
