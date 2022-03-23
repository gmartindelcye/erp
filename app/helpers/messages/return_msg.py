from urllib import response
from flask import jsonify
from app.helpers.messages.error_msg import *
from app.helpers.messages.success_msg import *
from flask import request

class MsgReturn:
    code = None
    app_code = None
    message = None
    data = False
    status = None
    row_total = None
    id_log = None
    
    def returns(self):
        if request.headers.get("Log-Id"):
            response = jsonify(
                code = self.code,
                app_code = self.app_code,
                message = self.message,
                data = self.data if self.data else "",
                id_log = request.headers.get("Log_Id")
            )
        else:
            response = jsonify(
                code = self.code,
                app_code = self.app_code,
                message = self.message,
                data = self.data if self.data else "",
                row_total = self.row_total if self.row_total else 0
            )
        response._status = self.status
        return response
    
    
    def custom_error_msg(self, code, app_code, message, status, id_log, data=""):
        response = jsonify(
                code = scode,
                app_code = app_code,
                message = message,
                data = data,
                id_log = id_log
            )
        response.status = status
        return response
        
    def error_id_not_found(self):
        self.code = ERROR_CODE_4041
        self.app_code = ERROR_CODE_4004
        self.message = ERROR_ID_NOT_FOUND
        self.data = ERROR_DATA
        self.status = ERROR_STATUS_404
        return self.returns()
    
    def actualizar(self, result):
        self.code = SUCCESS_CODE_2012
        self.app_code = SUCCESS_CODE_2012
        self.message = MSG_UPDATED_RECORD
        self.data = result
        self.status = SUCCESS_STATUS_200
        return self.returns()
    
    def consultar(self, result, row_total):
        self.code = SUCCESS_CODE_2001
        self.app_code = SUCCESS_CODE_2001
        self.message = MSG_OBTAINED_RECORD
        self.data = result
        self.row_total = row_total
        self.status = SUCCESS_CODE_200
        return self.returns()
    
    def crear(self,result):
        self.code = SUCCESS_CODE_2011
        self.app_code = SUCCESS_CODE_2011
        self.message = MSG_CREATED_RECORD
        self.data = result
        self.status = SUCCESS_MSG_201
        return self.returns()
    
    def eliminar(self):
        self.code = SUCCESS_CODE_2014
        self.app_code = SUCCESS_CODE_2014
        self.message = MSG_DELETED_RECORD
        self.status = SUCCESS_CODE_200
        return self.returns()
    
    def crear_database(self):
        self.code = SUCCESS_CODE_2001
        self.app_code = SUCCESS_CODE_2001
        self.message = SUCCESS_MSG_2001
        self.status = SUCCESS_MSG_201
        return self.returns()
    
    def eliminar_database(self):
        self.code = SUCCESS_CODE_2004
        self.app_code = SUCCESS_CODE_2004
        self.message = SUCCESS_MSG_2004
        self.status = SUCCESS_CODE_200
        return self.returns()
    
    def error_database(self, code, error):
        self.data = str(error)
        if code == ERROR_CODE_4200:
            self.code = ERROR_CODE_4200
            self.app_code = ERROR_CODE_4200
            self.message = ERROR_MSG_4200
        else:
            self.code = ERROR_CODE_4202
            self.app_code = ERROR_CODE_4202
            self.message = ERROR_MSG_4202
        self.status = ERROR_STATUS_404
        return self.returns()
    
    def custom_msg(self, code, app_code, message, status, data=""):
        self.code = code
        self.app_code = app_code
        self.message = message
        self.data = data
        self.status = status
        return self.returns()
    