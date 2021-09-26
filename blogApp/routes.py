from flask import render_template, url_for
from werkzeug.utils import redirect
from blogApp import app
from blogApp.forms import AuthorLogin


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/author', methods = ['GET','POST'])
def author():
    form = AuthorLogin()
    if form.validate_on_submit():
        if form.email.data == 'admin@mail.com' and form.password.data == 'admin':
            return redirect(url_for('index'))
    return render_template('login.html', form = form)