from app.config import APPLICATION_ROOT

def load_blueprints(instance):
    
    prefix = instance.config["APPLICATION_ROOT"]
    
    from .entityRoute import entity
    instance.register_blueprint(entity, url_prefix=prefix)