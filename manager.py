import logging

from flask_script import Manager, Server

from app import create_app
from app.utils import CommonJsonRet
from config import ENVI_DEV_KEY
from log import my_handler

app = create_app(ENVI_DEV_KEY)

manager = Manager(app)


@app.errorhandler(404)
def page_not_not_found(error):
    return CommonJsonRet(code=404,
                         success=False,
                         msg="404 Not Found . there is not this api",
                         data="").to_json_str()


@app.errorhandler(500)
def server_error(error):
    return CommonJsonRet(code=500,
                         success=False,
                         msg="server error",
                         data="").to_json_str()


# @app.errorhandler(401)
# def auth_error(error):
#     return CommonJsonRet(401, False, "Authentication error", {}).to_json_str()


manager.add_command("runserver", Server(host="0.0.0.0", port=9009))

# for logger in (
#         app.logger,
#         logging.getLogger('sqlalchemy'),
# ):
#     logger.addHandler(my_handler)

if __name__ == '__main__':
    manager.run()
