import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    AWS_KEY = os.environ.get('AWS_KEY')
    AWS_SECRET = os.environ.get('AWS_SECRET')
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
    AWS_S3_DOMAIN = f'https://{BUCKET_NAME}.s3-ap-southeast-1.amazonaws.com/'


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
