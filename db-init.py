from sqlalchemy import create_engine
from logger  import log

try:
    log.info('Initializing database')
    script = open('init.sql', 'r')
    engine = create_engine('postgresql://root:root@localhost:5432/db')
    engine.connect()
    engine.execute(script.read())
    engine.dispose()
    script.close()
    log.info('Successfuly initialized database')
except Exception as e:
    log.error(f"Error while initializing database: {e}")