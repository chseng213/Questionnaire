from flask_sqlalchemy import SQLAlchemy


def init_ext(app):
    # 初始化数据库
    init_db(app)


db = SQLAlchemy()


# 初始化数据库
def init_db(app):
    db.init_app(app)
