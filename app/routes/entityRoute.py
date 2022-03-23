from crypt import methods
from flask import Blueprint
from app.controllers.entityController import EntityController

entity = Blueprint("entity", __name__)

@entity.route('/entity', methods = ["POST"])
def new_entity():
    pass


@entity.route('/entity/<id>', methods = ["PATCH"])
def edit_entity(id: int):
    pass

@entity.route('/entity', methods = ["GET"])
def get_entities():
    pass

@entity.route('/entity/<id>', methods = ["GET"])
def get_entity(id: int):
    pass

@entity.route('/entity/<id>', methods = ["DELETE"])
def delete_entity(id: int):
    pass

