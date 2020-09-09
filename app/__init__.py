from flask import Flask

from app.urls import init_api
from config import environment
from ext_app import init_ext


def create_app(env_name="dev"):
    app = Flask(__name__)
    # 配置文件
    app.config.from_object(environment.get(env_name))
    # 第三方插件
    init_ext(app)
    init_api(app)
    return app
