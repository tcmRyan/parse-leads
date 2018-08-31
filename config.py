"""
Controls the configuration for all the different deployments of this
application
"""

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Configuration to be loaded into the heroku environment
    DO NOT CHECK IN
    """
    DEBUG = False
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']


class ProdConfig(Config):
    CSRF_ENABLED = True


class DevConfig(Config):
    DEBUG = True
