import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))

with open('/etc/config.json') as config_file:
        config = json.load(config_file)

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = config.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config.get('SECRET_KEY')
    POSTS_PER_PAGE = 6
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('MAIL_USERNAME')
    MAIL_PASSWORD = config.get('MAIL_PASSWORD')
