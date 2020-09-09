import logging
import os
from logging.config import dictConfig


def logger(logfile_name):
    # 定义简单的日志模式
    simple_format = '[%(levelname)s]\t[%(asctime)s] [%(filename)s][%(lineno)d] msg--> %(message)s'
    # 获取当前脚本的绝对路径
    logfile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log")
    if not os.path.isdir(logfile_dir): os.makedirs(logfile_dir)
    # log全路径
    logfile_path = os.path.join(logfile_dir, logfile_name)
    print(logfile_path)
    # 配置log字典
    LOGGING_DIC = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': simple_format,
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'filters': {},
        'handlers': {
            # 输出终端
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            # 输出文件
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'simple',
                'filename': logfile_path,
                'maxBytes': 1024 * 1024 * 10,  # 日志大小10M
                'backupCount': 5,
                'encoding': 'utf-8',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default', 'console'],
                'level': 'INFO',
                'propagate': True,  # 更高level传递
            },
        },
    }

    dictConfig(LOGGING_DIC)
    logger = logging.getLogger(__name__)
    return logger


my_handler = logger("apps.log")
