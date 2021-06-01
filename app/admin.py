from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from flask import redirect, url_for, request
from sqlalchemy import func
from wtforms.validators import required, Length
from app.models import User


class CustomStudentUser(ModelView):
    """Admin model, that available for all users. Users may just rename their email."""
    column_list = ("email",)
    column_editable_list = ['email', ]
    edit_modal = True
    form_excluded_columns = ["password", "active",
                             "interval_words", "words", "roles"]
    can_create = False
    form_args = {
        "email": {
            "label": "Email",
            "validators": [required(), Length(min=3, max=254)]
        }
    }

    def get_count_query(self):
        return self.session.query(func.count("*")). \
            filter(User.id == current_user.id)

    def get_query(self):
        return super(CustomStudentUser, self).get_query(). \
            filter(User.id == current_user.id)

    def get_one(self, id):
        query = self.get_query()
        return query.filter(User.id == id).one()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("security.login"))

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated)


class CustomAdminUser(ModelView):
    """Admin model, that available just for the admin. It permit to delete user account"""
    column_list = ("email",)
    column_searchable_list = ("email",)
    page_size = 20
    column_editable_list = ['email', ]
    edit_modal = True
    form_excluded_columns = ["interval_words", "words",
                             "password", "roles", "active"]
    can_create = False
    can_edit = False

    form_args = {
        "email": {
            "label": "Email",
            "validators": [required(), Length(min=3, max=254)]
        }
    }

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("security.login"))

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role("administrator"))


class CustomAdminVoc(ModelView):
    column_list = ("word", "translation")
    column_searchable_list = ("word", "translation")
    page_size = 50
    column_excluded_list = ["word", ]
    column_editable_list = ['word', 'translation']
    create_modal = True
    edit_modal = True
    form_excluded_columns = ["interval_users", "users", "learned_users"]

    form_args = {
        "word": {
            "label": "Слово",
            "validators": [required()]
        }
    }

    def get_count_query(self):
        return self.session.query(func.count("*")).select_from(self.model)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("security.login", next=request.url))

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role("administrator"))


class CustomAdminPhrasalVerbsVoc(ModelView):
    column_list = ("phrasal_verb", "translation")
    column_searchable_list = ("phrasal_verb", "translation")
    page_size = 50
    column_excluded_list = ["phrasal_verb", ]
    column_editable_list = ['phrasal_verb', 'translation']
    create_modal = True
    edit_modal = True
    form_excluded_columns = ["interval_users", "users", "learned_users"]

    form_args = {
        "phrasal_verb": {
            "label": "Слово",
            "validators": [required()]
        }
    }

    def get_count_query(self):
        return self.session.query(func.count("*")).select_from(self.model)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("security.login", next=request.url))

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role("administrator"))


class CustomAdminRole(ModelView):
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("security.login"))

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role("administrator"))

    # def is_accessible(self):
    #     return (current_user.is_active and
    #             current_user.is_authenticated)

    # def _handle_view(self, name, **kwargs):
    #     if not self.is_accessible:
    #         if current_user.is_autheticated:
    #             # permission denied
    #             abort(403)
    #         else:
    #             return self.inaccessible_callback(name, **kwargs)

# class CustomUserView(ModelView):
#     form = MyForm
#     column_list = ("email", "password")
#     column_list = ("email", )
#     column_searchable_list = ("email", )
#     page_size = 20
#     column_editable_list = ['email', ]
#     create_modal = True
#     edit_modal = True
#     form_excluded_columns = ["interval_words", "words", "password", "roles"]
#
#     def get_count_query(self):
#         return self.session.query(func.count("*")).\
#             filter(User.id == current_user.id)
#
#     def get_query(self):
#         return super(CustomUserView, self).get_query().\
#             filter(User.id == current_user.id)
#
#     def get_one(self, id):
#         query = self.get_query()
#         return query.filter(User.id == id).one()
