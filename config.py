"""
Controls the configuration for all the different deployments of this
application
"""

import os
import requests
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def ngrok_url():
    """
    Local Development redirect uri
    :return:
    """
    ngrok = os.environ['NGROK_URL']
    tunnels = requests.get(f'{ngrok}/api/tunnels').json()['tunnels']
    for tunnel in tunnels:
        if tunnel['proto'] == 'https':
            return tunnel['public_url']
    raise ValueError('No https tunnel available')


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
    ZOHO_OAUTH_CLIENT_ID = os.environ['ZOHO_OAUTH_CLIENT_ID']
    ZOHO_OAUTH_CLIENT_SECRET = os.environ['ZOHO_OAUTH_CLIENT_SECRET']


class ProdConfig(Config):
    CSRF_ENABLED = True
    BASE_URL = 'https://' + os.environ.get('HEROKU_APP_NAME', '') + '.herokuapp.com'


class DevConfig(Config):
    DEBUG = True
    # BASE_URL = ngrok_url()
    BASE_URL = 'https://e3255606.ngrok.io'
