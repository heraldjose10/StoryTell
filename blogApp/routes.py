from flask import render_template, url_for, redirect, request
from blogApp import app, bcrypt
from blogApp.forms import AuthorLogin
from blogApp.models import Authors, Blogs, Tags
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    blogs = Blogs.query.limit(9).all()
    return render_template('home.html', title = 'Home', blogs = blogs)

@app.route('/author', methods = ['GET','POST'])
def author():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AuthorLogin()
    if form.validate_on_submit():
        user = Authors.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
    return render_template('login.html', form = form)

@app.route('/blog/<blogid>')
def blogpage(blogid):
    blog = Blogs.query.get(int(blogid))
    return render_template('blogpage.html', blog = blog)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create_blog')
@login_required
def write():
    return current_user.name

@app.route('/tag/<tagName>')
def search(tagName):
    tag = Tags.query.filter_by(name = tagName).first()
    blogs = tag.blogs
    return render_template('tagSearchResults.html', searchResult = blogs, tag = tag)