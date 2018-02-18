class BaseConfig(object):
    """
    Common configurations
    """
    DEBUG = False
    TESTING = False
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Default timedelta(days=31) 2678400 seconds - Setting to 30 minutes = 1800 seconds
    # Note it requires session.permanent = True
    # To force session to expire if inactive only set session.modified = True
    # (set in home.py login route)
    PERMANENT_SESSION_LIFETIME = 1800

class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """
    DEBUG = True
    TESTING = True
    #SQLALCHEMY_ECHO = True
    #SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    """
    Production configurations
    """
    SESSION_COOKIE_SECURE = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
