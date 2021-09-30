from flask import render_template, url_for, redirect
from blogApp import app, bcrypt
from blogApp.forms import AuthorLogin
from blogApp.models import Authors, Blogs, Tags


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/author', methods = ['GET','POST'])
def author():
    form = AuthorLogin()
    if form.validate_on_submit():
        user = Authors.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            return redirect(url_for('index'))
    return render_template('login.html', form = form)