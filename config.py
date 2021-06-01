class Config:
    SECRET_KEY = 'r165er5efdytwefd56qre65wqfdty'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:" \
                              "123456@localhost/my_project"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_BLUEPRINT_NAME = "security"
    SECURITY_LOGOUT_URL = "/logout"
    SECURITY_PASSWORD_SALT = "78ry3487tyf34yuhfy73t"
    SECURITY_POST_LOGIN_VIEW = "/main/"
    SECURITY_POST_LOGOUT_VIEW = "/main/"
    SECURITY_POST_REGISTER_VIEW = "/main/"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    LANGUAGES = ["en", "ru", "es"]
    BABEL_DEFAULT_LOCALE = "ru"
    FLASK_ADMIN_SWATCH = "cerulean"
    roles = [
        {"name": "student",
         "description": "Just learn English and worry nothing, may change email"
         },
        {"name": "editor",
         "description": "allowed to correct the words-translations"
         },
        {"name": "administrator",
         "description": "full access"
         }
    ]


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:" \
                              "123456@localhost/my_project"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = "78ry3487tyf34yuhfy73t"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False


class Configuration(object):
    # SECRET_KEY = os.environ["SECRET_KEY"]
    WHOOSH_BASE = "whoosh"
    # SECURITY_REGISTER_URL = "/create_account"


config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,
}
