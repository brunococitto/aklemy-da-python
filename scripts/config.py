from logger import log
from decouple import config
from ast import literal_eval

class Config:
    """
        This class loads configuration from .env file on constructor method
    """
    def __init__(self):
        log.info("Starting to load configuration from .env file")
        DB_PARAMS = {'DB_USER':'root', 'DB_PASSWORD':'root', 'DB_HOST':'localhost', 'DB_PORT':'5432', 'DB_NAME':'db'}
        for param in DB_PARAMS:
            DB_PARAMS[param] = config(param, default=DB_PARAMS[param], cast=str)
        self.DB_URI = f"postgresql://{DB_PARAMS['DB_USER']}:{DB_PARAMS['DB_PASSWORD']}@{DB_PARAMS['DB_HOST']}:{DB_PARAMS['DB_PORT']}/{DB_PARAMS['DB_NAME']}"

        self.SOURCES = config('SOURCES', default="[]", cast=literal_eval)
        log.info("Configuration loaded successfuly")

if __name__ == '__main__':
    config = Config()