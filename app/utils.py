import json
import sys
from functools import wraps

import requests
import six
from flask import request, abort, current_app, got_request_exception
from flask_restful import Api
from flask_restful.reqparse import Argument, RequestParser, Namespace
from werkzeug import exceptions
from werkzeug.datastructures import Headers
from werkzeug.exceptions import HTTPException

AUTH_URL = "https://apiv7.scoreradar.net/v1/auth/check"
WTOKEN = "fcg-E3jOeQe8Zz8"


class CodeMsg:
    class CM:
        def __init__(self, code, msg):
            self.code = code
            self.msg = msg

    SUCCESS = CM(200, "成功")
    TIMEOUT = CM(404, "超过截止时间")
    AUTH_FAILED = CM(401, "用户认证失败")


# class CommonApi(Api):
#     def handle_error(self, e):
#         """
#
#         :param e: the raised Exception object
#         :type e: Exception
#
#         """
#         got_request_exception.send(current_app._get_current_object(), exception=e)
#
#         if not isinstance(e, HTTPException) and current_app.propagate_exceptions:
#             exc_type, exc_value, tb = sys.exc_info()
#             if exc_value is e:
#                 raise
#             else:
#                 raise e
#
#         headers = Headers()
#         if isinstance(e, HTTPException):
#             if e.response is not None:
#                 # If HTTPException is initialized with a response, then return e.get_response().
#                 # This prevents specified error response from being overridden.
#                 # eg. HTTPException(response=Response("Hello World"))
#                 resp = e.get_response()
#                 return resp
#
#             code = e.code
#             default_data = {
#                 'message': getattr(e, 'description', http_status_message(code))
#             }
#             headers = e.get_response().headers
#         else:
#             code = 500
#             default_data = {
#                 'message': http_status_message(code),
#             }
#
#         # Werkzeug exceptions generate a content-length header which is added
#         # to the response in addition to the actual content-length header
#         # https://github.com/flask-restful/flask-restful/issues/534
#         remove_headers = ('Content-Length',)
#
#         for header in remove_headers:
#             headers.pop(header, None)
#
#         data = getattr(e, 'data', default_data)
#
#         if code and code >= 500:
#             exc_info = sys.exc_info()
#             if exc_info[1] is None:
#                 exc_info = None
#             current_app.log_exception(exc_info)
#
#         error_cls_name = type(e).__name__
#         if error_cls_name in self.errors:
#             custom_data = self.errors.get(error_cls_name, {})
#             code = custom_data.get('status', 500)
#             data.update(custom_data)
#
#         if code == 406 and self.default_mediatype is None:
#             # if we are handling NotAcceptable (406), make sure that
#             # make_response uses a representation we support as the
#             # default mediatype (so that make_response doesn't throw
#             # another NotAcceptable error).
#             supported_mediatypes = list(self.representations.keys())
#             fallback_mediatype = supported_mediatypes[0] if supported_mediatypes else "text/plain"
#             resp = self.make_response(
#                 data,
#                 code,
#                 headers,
#                 fallback_mediatype = fallback_mediatype
#             )
#         else:
#             resp = self.make_response(data, code, headers)
#
#         if code == 401:
#             resp = self.unauthorized(resp)
#         return resp

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
