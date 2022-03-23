
import os
from dataclasses import dataclass
from os.path import join, dirname, abspath

from app.config import LOCALDBNAME, TESTDBNAME, db_uri


basedir = abspath(dirname(__file__))
dbpath = join(basedir,'database')
localdb = join(dbpath, LOCALDBNAME)
testdb = join(dbpath, TESTDBNAME)

@dataclass
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    
@dataclass 
class LocalDBConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + localdb
    
@dataclass 
class LocalConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db_uri()
    
@dataclass 
class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + testdb
    

config = {
    'LOCALDB' : LocalDBConfig,
    'LOCAL': LocalConfig,
    'TEST' : TestConfig,
}
    
    