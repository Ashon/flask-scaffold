import os

env = os.environ

# Flask
DEBUG = env.get('DEBUG') == 'True'

LOGGING = {
    'version': 1,
    'root': {
        'level': 'INFO',
    }
}
SALT = 'aosidjfoaisjdflkwejfo'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = env.get('DB_URI', 'sqlite:///db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-smorest
API_TITLE = 'Test API'
API_VERSION = 'v1'
API_DESCRIPTION = """
Test API
"""

OPENAPI_VERSION = '3.0.2'
OPENAPI_URL_PREFIX = '/'
OPENAPI_JSON_PATH = 'api-spec.json'
OPENAPI_SWAGGER_UI_PATH = '/apidoc'
OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.40.0/'
