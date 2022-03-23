from email import message
from urllib import response
from sqlalchemy import ForeignKey
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, Unauthorized, Forbidden, MethodNotAllowed
from werkzeug.exceptions import RequestTimeout, UnprocessableEntity, BadRequest
from marshmallow.exceptions import ValidationError

from app.helpers.messages.return_msg import MsgReturn
from app.helpers.messages.error_msg import *

class HandlerErrors:
    data = ""
    message = ERROR_MSG_5000
    app_code = ERROR_CODE_5000
    code = ERROR_CODE_5000
    status = ERROR_STATUS_500
    
    @staticmethod
    def handler_middleware_errors(error: Exception, id_log=0):
        message = ERROR_MSG_5000
        app_code = ERROR_CODE_5000
        code = ERROR_CODE_5000
        status = ERROR_STATUS_500
        data = str(error.__class__)
        
        if isinstance(error, Unauthorized):
            message = ERROR_MSG_4001
            app_code = ERROR_CODE_4001
            code = ERROR_CODE_4001
            status = ERROR_STATUS_401
        elif isinstance(error, Forbidden):
            message = ERROR_MSG_4003
            app_code = ERROR_CODE_4003
            code = ERROR_CODE_4003
            status = ERROR_STATUS_403
        elif isinstance(error KeyError):
            message = f"{ERROR_MSG_4104}: {error}"
            app_code = ERROR_CODE_4104
            code = ERROR_CODE_4104
            status = ERROR_STATUS_404
        elif isinstance(error, IntegrityError):
            if ('UniqueViolation' in error.args[0]):
                message = ERROR_MSG_4204
                app_code = ERROR_CODE_4204
                code = ERROR_CODE_4204
                status = ERROR_STATUS_400
            elif ('ForeignKeyViolation' in error.args[0]):
                message = ERROR_MSG_4205
                app_code = ERROR_CODE_4205
                code = ERROR_CODE_4205
                status = ERROR_STATUS_404
            elif ('NotNullViolation' in error.args[0]):
                message = ERROR_MSG_4206
                app_code = ERROR_CODE_4206
                code = ERROR_CODE_4206
                status = ERROR_STATUS_400
            else:
                message = ERROR_MSG_4201
                app_code = ERROR_CODE_4201
                code = ERROR_CODE_4201
                status = ERROR_STATUS_400
        elif isinstance(error, ValidationError):
            message = ERROR_MSG_4304
            app_code = ERROR_CODE_4304
            code = ERROR_CODE_4304
            status = ERROR_STATUS_404
            
        if id_log != 0:
            return MsgReturn().custom_error_msg(code, app_code, message, status, id_log, data)
        
        response = MsgReturn().custom_msg(code, app_code, message, status, data)
        response._status = status
        return response
    
    @staticmethod
    def handler_http_error(error: Exception):
        message = ERROR_MSG_5000
        app_code = ERROR_CODE_5000
        code = ERROR_CODE_5000
        data = str(error.__class__)
        status = ERROR_STATUS_500
        
        if isinstance(error, NotFound):
            message = ERROR_MSG_4004
            app_code = ERROR_CODE_4004
            code = ERROR_CODE_4004
            status = ERROR_STATUS_404
        elif isinstance(error, BadRequest):
            message = ERROR_MSG_4000
            app_code = ERROR_CODE_4000
            code = ERROR_CODE_4000
            status = ERROR_STATUS_400
        elif isinstance(error, MethodNotAllowed):
            message = ERROR_MSG_4005
            app_code = ERROR_CODE_4005
            code = ERROR_CODE_4005
            status = ERROR_STATUS_405
        elif isinstance(error, RequestTimeout):
            message = ERROR_MSG_4008
            app_code = ERROR_CODE_4008
            code = ERROR_CODE_4008
            status = ERROR_STATUS_408
        elif isinstance(error, UnprocessableEntity):
            message = ERROR_MSG_4022
            app_code = ERROR_CODE_4022
            code = ERROR_CODE_4022
            status = ERROR_STATUS_400

        response = MsgReturn().custom_msg(code, app_code, message, status, data)
        response._status = status
        return response
    
            


                




