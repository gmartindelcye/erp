from socket import has_ipv6
from unittest import result

from attr import dataclass
from app.helpers.messages.error_msg import ERROR_CODE_4201, ERROR_DATA_4201, ERROR_STATUS_405
from app.helpers.messages.error_msg import ERROR_MSG_4201, ERROR_CODE_4201
from app.helpers.messages.return_msg import MsgReturn
from app.helpers.handler.handler_errors import HandlerErrors
from app.models import db
from flask import request
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import ImmutableMultiDict


class BaseController:
    model = None
    data_json = request.get_json()
    schema = None
    creationSchema = None
    rules = None
    
    def check_result(self,result):
        if str(self.model) == "<class 'app.models.transTypeModel.TransType'>":
            if str(type(result)) == "class <'flask_sqlalchemy.Pagination'>":
                for n in range(len(result.items)):
                    if result.items[n].reverso_id != None:
                        if result.items[n].reversos.reverso_id != None:
                            result.items[n].reversos.reverso_id = None
                            result.items[n].reversos.reversos = None
            else:
                print("Entra2!")
                try:
                    if result.reversos.reversos.reverso_id != None:
                        result.reversos.reversos.reverso_id = None
                        result.reversos.reversos.reversos = None
                except:
                    pass
        return result
    
    
    def check_datetime(self, date_creacion, date_modificacion):
        new_date_modificacion = datetime.strptime(date_modificacion,'%Y-%m-%d %H:%M:%S')
        new_date_creacion = datetime.strptime(date_creacion,'%Y-%m-%d %H:%M:%S')
        return new_date_modificacion <= new_date_creacion
    
    
    def upper_string_values(self, dict_data):
        for key in dict_data.keys():
            value = dict_data[key]
            if isinstance(value, str):
                dict_data[key] = value.upper()
        return dict_data
    
    
    def actualizar(self, identificador):
        self.data_json = request.get_json()
        result = self.model.query.filter_by(id=identificador)
        if not result.first():
            return MsgReturn().error_id_not_found()
        schema = self.creationSchema()
        result.update(self.data_json)
        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            return HandlerErrors.handler_middleware_errors(error)
        return MsgReturn().actualizar(result.first().to_dict())


    def consulta_individual(self, identificador):
        result = self.model.query.filter_by(id==identificador).first()
        if not result:
            return MsgReturn().error_id_not_found()
        
        result = self.check_result(result)
        
        if self.rules != None:
            data = result.to_dict(rules=self.rules)
        else:
            data = result.to_dict()
            
        return MsgReturn().consultar(data,1)
    
    
    def consulta_general(self):
        data_args = request.args
        page = data_args.get('page', 1, type=int)
        limit = data_args.get('limit', 10, type=int)
        result = self.model.query.order_by(self.model.id.asc()).paginate(page, per_page=limit, error_out=False)
        
        if len(result.items) == 0:
            return MsgReturn().error_id_not_found
        
        result = self.check_result(result)
        
        if self.rules != None:
            data = [r.to_dict(rules=self.rules) for r in result.items]
        else:
            data = [r.to_dict() for r in result.items]
        
        return MsgReturn().consultar(data, result.total)
    
    
    def crear(self):
        dataset = {}
        for key, value in request.get_json().items():
            if str(type(value)) == "<class 'str>":
                value = str(value).replace("\r", " ").replace("\n", " ")
            dataset[key] = value
        
        self.data_json = dataset
        keys = self.data_json.keys()
        if "fecha_creacion" in keys and "fecha_edicion" in keys:
            has_wrong_datetime = self.check_datetime(self.data_json["fecha_creacion"], self.data_json["fecha_edicion"])
            if has_wrong_datetime:
                return MsgReturn().custom_msg(ERROR_CODE_4201, ERROR_CODE_4201, 
                                              ERROR_MSG_4201, ERROR_STATUS_405, ERROR_DATA_4201)
                
        schema = self.creationSchema()
        self.upper_string_values(self.data_json)
        valid_data = schema.load(self.data_json)
        record = self.model(**valid_data)
        try:
            db.session.add(record)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            return HandlerErrors.handler_middleware_errors(error)
        return MsgReturn().crear(record.to_dict())
    
    
    def eliminar(self, identificador):
        result = self.model.query.filter_by(id==identificador).first()
        if not result:
            return MsgReturn().error_id_not_found()
        try:
            db.session.delete(result)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            return HandlerErrors.handler_middleware_errors(error)
        return MsgReturn().eliminar()
    
    
    def _paginar(self, queryset, argumentos: ImmutableMultiDict):
        page = argumentos.get('page', 1, type=int)
        limit = argumentos.get('limit', 10, type=int)
        return queryset.paginate(page, per_page=limit, error_out=False)
                