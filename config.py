import os


class Config(object):
    ROOT = os.path.dirname(os.path.abspath(__file__))
    LOG_NAME = os.path.join(ROOT, 'logs', 'rocket.log')

    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_PWD = '123456'
    MYSQL_PORT = 3306
    DBNAME = 'rocket'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{DBNAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_KEY = 'rocket'
    TOKEN_EXPIRATION = 3
