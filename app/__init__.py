from flask import Flask
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_security import SQLAlchemyUserDatastore, Security
from app.admin import CustomAdminVoc, CustomAdminUser, \
    CustomAdminRole, CustomStudentUser, CustomAdminPhrasalVerbsVoc
from app.forms import MyCustomLoginForm
from app.models import db, User, Role, Vocabulary, PhrasalVerbsVocabulary
from config import Config
from sqlalchemy import exc as sa_exc

admin = Admin(name="Admin panel", template_mode="bootstrap4")
babel = Babel()
bootstrap = Bootstrap()
security = Security()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    admin.init_app(app)
    babel.init_app(app)
    bootstrap.init_app(app)
    security.init_app(app, user_datastore,
                      login_form=MyCustomLoginForm)

    from app.ir_voc.ir_vocabulary import ir_voc
    from app.voc.vocabulary import voc
    from app.word_test.word_test import word_test_bp
    from app.main.main_bp import main
    from app.error_pages.error_pages import error_403, \
        error_404, error_500, error_pages_bp

    app.register_blueprint(voc, url_prefix="/voc")
    app.register_blueprint(ir_voc, url_prefix="/ir_voc")
    app.register_blueprint(word_test_bp, url_prefix="/word_test")
    app.register_blueprint(main, url_prefix="/main")
    app.register_blueprint(error_pages_bp, url_prefix="/")
    app.register_error_handler(403, error_403)
    app.register_error_handler(404, error_404)
    app.register_error_handler(500, error_500)
    """The initial database creating"""
    with app.app_context():
        db.create_all()
        configuration = Config()
        for role_desc in configuration.roles:
            try:
                user_datastore.find_or_create_role(**role_desc)
                db.session.commit()
            except sa_exc.IntegrityError:
                db.session.rollback()

    admin.add_view(CustomAdminVoc(Vocabulary, db.session))
    admin.add_view(CustomAdminUser(User, db.session))
    admin.add_view(CustomAdminRole(Role, db.session))
    admin.add_view(CustomStudentUser(User, db.session, name="Student",
                                     url="student", endpoint="stud"))
    admin.add_view(CustomAdminPhrasalVerbsVoc(PhrasalVerbsVocabulary, db.session))
    link = app.config['SECURITY_BLUEPRINT_NAME'] + app.config['SECURITY_LOGOUT_URL']
    admin.add_link(MenuLink(name="Выйти", url=link))
    admin.add_link(MenuLink(name="На главную", url="/main/"))
    return app
