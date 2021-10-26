from flask import render_template
from blogApp import db
from blogApp.errors import bp


@bp.app_errorhandler(404)
def error_404(error):
    """function for handling not found errors

    Parameters
    ----------
    error : werkzeug.exceptions object
    """
    error_heading = "You seem lost !"
    title = '404 Not Found'
    return render_template('errors/404.html', title=title, error_heading=error_heading), 404


@bp.app_errorhandler(403)
def error_403(error):
    """function for handling 403 errors

    Parameters
    ----------
    error : werkzeug.exceptions object
    """
    error_heading = "You are getting in trouble for that !"
    title = '403 Forbidden'
    return render_template('errors/403.html', title=title, error_heading=error_heading), 403


@bp.app_errorhandler(500)
def error_500(error):
    """function for handling internal errors

    Parameters
    ----------
    error : werkzeug.exceptions object
    """
    db.session.rollback()  # rolls back all session changes to database
    error_heading = "It seems our servers are on fire !"
    title = '500 Internal Error'
    return render_template('errors/500.html', title=title, error_heading=error_heading), 500
