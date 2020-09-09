# 开发环境映射
import os
import sys

# 数据库参数
DATABASE = {
    'product':
        {
            'ENGINE': 'mysql',
            # 'HOST': '192.168.2.222',
            'HOST': '47.244.91.219',
            'PASSWORD': '@GoTo1024',
            'USER': 'fcgsports',
            'PORT': '3306',
            'NAME': 'fcgsports',
            "CHARSET": "utf8"
        },
    'default':
        {
            'ENGINE': 'mysql',
            'HOST': '192.168.2.222',
            'PORT': '3306',
            'NAME': 'fcgsports',
            "CHARSET": "utf8"
        }

}


def get_db_uri(database: dict):
    """
    获取数据库的URI
    生成数据连接 dialect+driver://username:password@host:port/database
    :param database:
    :return:
    """
    engine = database.get('ENGINE') or 'mysql'
    user = database.get('USER') or 'root'
    password = database.get('PASSWORD') or 'root5678'
    driver = database.get('DRIVER') or 'pymysql'
    host = database.get('HOST') or '127.0.0.1'
    port = database.get('PORT') or '3306'
    name = database.get('NAME')
    charset = database.get('CHARSET') or 'utf8'
    return "{}+{}://{}:{}@{}:{}/{}?charset={}".format(engine, driver, user, password, host, port, name, charset)


class BaseConfig:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_POOL_SIZE = 500
    SQLALCHEMY_POOL_RECYCLE = 1600


# 开发环境配置
class DeveloperConfig(BaseConfig):
    # DEBUG = True
    # 秘钥
    SECRET_KEY = '123456'
    # 输出sql语句
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE.get('default'))


# 生产环境配置
class ProductConfig(BaseConfig):
    SECRET_KEY = '4ce01aa944434ff4880b29b0992ee846'
    # 生成环境小设置连接池的数量
    # SQLALCHEMY_POOL_SIZE = 200
    # 配置数据连接路径
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE.get('product'))


# 服务环境
ENVI_DEV_KEY = 'product' if sys.platform == "linux" else "dev"

environment = {
    'dev': DeveloperConfig,
    'product': ProductConfig
}
