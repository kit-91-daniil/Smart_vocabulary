from flask import Blueprint, render_template

error_pages_bp = Blueprint("error_pages", __name__,
                        template_folder="templates", static_folder="static")


@error_pages_bp.errorhandler(404)
def error_404(e):
    return render_template("error_pages/404.html"), 404


@error_pages_bp.errorhandler(403)
def error_403(e):
    return render_template("error_pages/403.html"), 403


@error_pages_bp.errorhandler(500)
def error_500(e):
    return render_template("error_pages/500.html"), 500
