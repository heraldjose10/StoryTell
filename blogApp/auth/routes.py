from blogApp.auth.forms import AuthorLogin, RegisterForm, NewPasswordForm, PasswordResetForm
from flask import redirect, render_template, url_for, request
from blogApp.models import Authors
from flask_login import current_user, login_user, login_required, logout_user
from blogApp import db
from blogApp.auth import email, bp


@bp.route('/author', methods=['GET', 'POST'])
def author():
    """Route for logging in authors/users"""
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = AuthorLogin()
    if form.validate_on_submit():
        user = Authors.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # login if user exists and password checks out
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # redirect to next page after logging in if next page exists or redirect to homepage
            return redirect(next_page) if next_page else redirect(url_for('core.index'))

    return render_template('login.html', title='Login', form=form)


@bp.route('/logout')
@login_required
def logout():
    """Route for logging out authors/users"""
    logout_user()
    return redirect(url_for('core.index'))


@bp.route('/register', methods=['GET', 'POST'])
def signup():
    """Route for registering authors/users"""
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        # create new author object
        author = Authors(name=form.name.data, email=form.email.data)
        # set password for newly created author
        author.set_password(form.password.data)
        db.session.add(author)  # add newly created author to database
        db.session.commit()
        return redirect('author')  # redirect to login page

    return render_template('register.html', title='Register', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_pass_request():
    """Route for requesting reset password mail"""
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        user = Authors.query.filter_by(email=form.email.data).first()
        if user:
            # send mail to mail id if a suer with the mail id exists
            email.send_pass_reset_mail(user)
        return redirect(url_for('auth.author'))  # redirect to login page

    return render_template('password_reset_form.html', title='reset password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Resets password of user 

    Parameters
    ----------
    token : encoded JSON web token
    """
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = NewPasswordForm()
    # verifies if token is valid and is not expired
    user = Authors.verify_password_reset_token(token)

    if user == None:
        return redirect(url_for('core.index'))

    if form.validate_on_submit():
        # sets new password for user
        user.set_password(form.create_password.data)
        db.session.commit()
        return redirect(url_for('auth.author'))  # redirect to login page

    return render_template('create_new_password.html', form=form, title='new password')
