from flask import Blueprint, render_template, current_app
from flask_security import login_required, current_user
from app import user_datastore
from app.models import db
from app import Config

main = Blueprint("main", __name__, template_folder="templates",
                 static_folder="static"
                 )


@main.route("/")
@login_required
def personal_room():
    config_inst = Config()
    roles_accepted = [role_name["name"] for role_name in config_inst.roles]
    if not any([current_user.has_role(role) for role in roles_accepted]):
        default_role = user_datastore.find_role("student")
        user_datastore.add_role_to_user(current_user, default_role)
        db.session.commit()
    return render_template("main/personal_room.html")


if __name__ == "__main__":
    pass
