import json
# import sys
import time
from functools import wraps

import requests
import six
from flask import request, abort, current_app, got_request_exception, jsonify
# from flask_restful import Api
from flask_restful import Api
from flask_restful.reqparse import Argument, RequestParser, Namespace
from werkzeug import exceptions
# from werkzeug.datastructures import Headers
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

AUTH_URL = "https://apiv7.scoreradar.net/v1/auth/check"
AUTH_URL = "http://47.56.109.14:8081/v1/auth/check"
OSS_URL = "https://cdn.scoreradar.live/scoreradar/team/{}.png"
WTOKEN = "fcg-E3jOeQe8Zz8"


def get_order_code():
    """
    生成简易的订单编号
    :return:
    """
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')[-8:]
    return order_no


class CodeMsg:
    class CM:
        def __init__(self, code, msg):
            self.code = code
            self.msg = msg

    SUCCESS = CM(200, "成功")
    TIMEOUT = CM(404, "超过截止时间")
    AUTH_FAILED = CM(401, "用户认证失败")


class ExtendedAPI(Api):
    """This class overrides 'handle_error' method of 'Api' class ,
    to extend global exception handing functionality of 'flask-restful'.
    """

    def handle_error(self, err):
        """It helps preventing writing unnecessary
        try/except block though out the application
        """
        # log every exception raised in the application
        # Handle HTTPExceptions
        if isinstance(err, HTTPException):
            return jsonify(err.data), 200
        # If msg attribute is not set,
        # consider it as Python core exception and
        # hide sensitive error info from end user
        if not getattr(err, 'message', None):
            return jsonify({
                'message': 'Server has encountered some error'
            }), 200
        # Handle application specific custom exceptions
        return jsonify(**err.kwargs), 200


def common_abort(http_status_code, **kwargs):
    """Raise a HTTPException for the given http_status_code. Attach any keyword
    arguments to the exception for later processing.
    """
    # noinspection PyUnresolvedReferences
    try:
        abort(http_status_code)
    except HTTPException as e:
        if len(kwargs):
            e.data = kwargs
        raise


class CommonJsonRet:
    def __init__(self, code, success, msg, data):
        self.code = code
        self.msg = msg
        self.data = data
        self.success = success

    def to_json_str(self):
        return json.dumps(self.__dict__)

    def to_json(self):
        return self.__dict__

    def __call__(self, *args, **kwargs):
        return self.to_json()


class AuthToken:

    def auth_token(self, url, token):
        res = {}
        i = 0
        while i < 3:
            try:
                res = requests.get(url,
                                   headers={
                                       'Authorization': token
                                   })

                print(res.json())
                break
            except:
                i += 1
        if (not res) or (not res.json().get("data")):
            common_abort(401, **{
                "code": 401,
                "msg": "Authentication error",
                "data": {},
                "success": False
            })
        user_id = res.json().get("data").get("userId")

        return user_id

    def __call__(self, func):
        @wraps(func)
        def wrap(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return CommonJsonRet(401, False, "Authentication error", {}).to_json()
            user_id = self.auth_token(AUTH_URL, token)

            resp = func(*args, **kwargs, user_id=user_id)
            return resp

        return wrap


class CommonResponse:
    def __init__(self, code, success, msg, data):
        self.data = data
        self.success = success
        self.code = code
        self.msg = msg

    def __call__(self):
        return CommonJsonRet(self.code, self.success, self.msg, self.data).to_json()


class CommonArgument(Argument):
    def handle_validation_error(self, error, bundle_errors):
        error_str = six.text_type(error)
        error_msg = ' '.join([six.text_type(self.help), error_str]) if self.help else error_str
        msg = {self.name: error_msg}

        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
            return error, msg
        common_abort(400, **{
            "code": 400,
            "msg": msg,
            "data": {},
            "success": False
        })


class CommonRequestParser(RequestParser):
    def __init__(self, argument_class=CommonArgument, namespace_class=Namespace,
                 trim=False, bundle_errors=False):
        self.args = []
        self.argument_class = argument_class
        self.namespace_class = namespace_class
        self.trim = trim
        self.bundle_errors = bundle_errors

    def parse_args(self, req=None, strict=False, http_error_code=400):
        if req is None:
            req = request

        namespace = self.namespace_class()

        req.unparsed_arguments = dict(self.argument_class('').source(req)) if strict else {}
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                namespace[arg.dest or arg.name] = value
        if errors:
            common_abort(http_error_code, **{
                "code": http_error_code,
                "msg": errors,
                "data": {},
                "success": False
            })

        if strict and req.unparsed_arguments:
            arguments = ', '.join(req.unparsed_arguments.keys())
            msg = 'Unknown arguments: {0}'.format(arguments)
            raise exceptions.BadRequest(msg)

        return namespace
