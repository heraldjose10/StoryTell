from blogApp.auth.forms import AuthorLogin, RegisterForm, NewPasswordForm, PasswordResetForm
from flask import redirect, render_template, url_for, request
from blogApp.models import Authors
from flask_login import current_user, login_user, login_required, logout_user
from blogApp import db, bcrypt
from blogApp.auth import email, bp


@bp.route('/author', methods=['GET', 'POST'])
def author():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = AuthorLogin()
    if form.validate_on_submit():
        user = Authors.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('core.index'))
    return render_template('login.html', title='Login', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@bp.route('/register', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        author = Authors(name=form.name.data, email=form.email.data,
                         password=bcrypt.generate_password_hash(form.password.data))
        db.session.add(author)
        db.session.commit()
        return redirect('author')
    return render_template('register.html', title='Register', form=form)


@bp.route('/reset_password_request', methods = ['GET', 'POST'])
def reset_pass_request():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = Authors.query.filter_by(email = form.email.data).first()
        if user:
            email.send_pass_reset_mail(user)
        return redirect(url_for('auth.author'))
    return render_template('password_reset_form.html', title = 'reset password', form = form)


@bp.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = NewPasswordForm()
    user = Authors.verify_password_reset_token(token)
    if user == None:
        return redirect(url_for('core.index'))
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.create_password.data)
        db.session.commit()
        return redirect(url_for('auth.author'))       
    return render_template('create_new_password.html', form = form, title = 'new password')