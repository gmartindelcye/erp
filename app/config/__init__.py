# app > config

LOCALDBNAME = 'database.db'
TESTDBNAME = 'test.db'

APPLICATION_ROOT = '/'

def db_uri():
    header = 'postgresql+psycopg2'
    server = '127.0.0.1'
    port = '5432'
    user = 'erpuser'
    pssw = 'erppassw'
    db = 'erp'
    
    return f"{header}://{user}:{pss}@{server}:{port}/{db}"