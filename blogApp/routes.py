from flask import render_template, url_for, redirect
from blogApp import app, bcrypt
from blogApp.forms import AuthorLogin
from blogApp.models import Authors, Blogs, Tags


@app.route('/')
def index():
    blogs = Blogs.query.limit(9).all()
    return render_template('home.html', title = 'Home', blogs = blogs)

@app.route('/author', methods = ['GET','POST'])
def author():
    form = AuthorLogin()
    if form.validate_on_submit():
        user = Authors.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            return redirect(url_for('index'))
    return render_template('login.html', form = form)

@app.route('/blog/<blogid>')
def blogpage(blogid):
    blog = Blogs.query.get(int(blogid))
    return render_template('blogpage.html', blog = blog)