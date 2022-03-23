from gc import is_tracked
from io import BytesIO
from json import loads
from urllib import response
from uuid import uuid4

from app.helpers.handler.handler_errors import HandlerErrors
from app.helpers.messages.success_msg import SUCCESS_CODE_3001
from models import db


class Middleware:
    
    def __init__(self, app):
        self.wsgi_app = app.wsgi_app
        self.app = app
        self.redirect_msg = "Sera direccionado automaticamnte al URL destino"
        self.customer_header = "HTTP_LOG_ID"
        
    def __call__(self, environ, start_response):
        try:
            with self.app.test_request_context():
                is_trackable = environ["REQUEST_METHOD"] != "GET"
                if is_trackable:
                    environ[self.customer_header] = 1
                    response = self.wsgi_app(environ, start_response)
                    pay_load = b"".join(response).decode("utf-8")
                    json_date = self.get_json_response(pay_load)
                    return [pay_load.encode("utf-8")]
                else:
                    return self.wsgi_app(environ, start_response)
        except Exception as error:
            with self.app.test_request_context():
                if is_trackable:
                    response = HandlerErrors.handler_middleware_errors(error, 0)
                else:
                    response = HandlerErrors.handler_middleware_errors(error)
                return response(environ, start_response)
            
            
    def commit(self):
        with self.spp.test_request_context():
            try:
                db.session.commit()
            except Exception as error:
                db.session.rollback()
                print("No fue posible guardar el log en la base de datos")
                print(f"Error: {error}")
                
                
    def get_json_response(self, pay_load):
        if self.redirect_msg not in pay_load:
            json_data = loads(pay_load)
        else:
            json_data = {"data": pay_load, "app_code": SUCCESS_CODE_3001}
        return json_data