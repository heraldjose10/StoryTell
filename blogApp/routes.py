import secrets
import bleach
import os
import base64
from flask import render_template, url_for, redirect, request, abort
from blogApp import app, bcrypt, db
from blogApp.forms import AuthorLogin, RegisterForm, BlogForm, ProfileForm
from blogApp.models import Authors, Blogs, Tags
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    blogs = Blogs.query.order_by(Blogs._created.desc()).limit(6).all()
    return render_template('home.html', title='Home', blogs=blogs)


@app.route('/author', methods=['GET', 'POST'])
def author():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AuthorLogin()
    if form.validate_on_submit():
        user = Authors.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)


@app.route('/blog/<blogid>')
def blogpage(blogid):
    blog = Blogs.query.get(int(blogid))
    # format = "%d/%m/%Y"
    # print(blog._created.strftime(format))
    return render_template('blogpage.html', blog=blog)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_file(file, path):
    file = file.partition(",")[2]
    random_hex = secrets.token_hex(8)
    updated_file_name = random_hex+'.jpeg'
    file_path = os.path.join(app.root_path, path, updated_file_name)

    with open(file_path, 'wb') as fh:
        fh.write(base64.decodebytes(bytes(file, 'utf-8')))

    return updated_file_name


def bleach_tags(to_bleach):
    allowed_tags = ['span', 'p', 'img', 'a', 'br', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'u',
                        'blockquote', 'font', 'iframe', 'pre', 'ol', 'li', 'ul', 'div', 'table', 'tbody', 'td', 'tr']
    attrs = {
        '*': ['style', 'color', 'class'],
        'div': ['bis_skin_checked'],
        'a': ['href', 'target'],
        'img': ['src', 'class'],
        'iframe': ['frameborder', 'src', 'width', 'height']
    }
    styles = ['background-color', 'text-align',
                'margin-left', 'width', 'float']
    clean_content = bleach.clean(
        to_bleach, tags=allowed_tags, attributes=attrs, styles=styles)
    return(clean_content)


@app.route('/create_blog', methods=['Get', 'POST'])
@login_required
def write():
    form = BlogForm()
    if form.validate_on_submit():
        tags = form.tags.data.split(' ')[:-1]
        content = form.editordata.data
        cleaned = bleach_tags(content)
        blog = Blogs(title=form.title.data,
                     content=cleaned, author=current_user)
        db.session.add(blog)
        if form.thumbnail_data.data:
            img_data = form.thumbnail_data.data
            thumbnail_name = save_file(img_data, 'static/assets/thumbnails/')
            blog.thumbnail = thumbnail_name
        for tag in tags:
            t = Tags.query.filter_by(name=tag).first()
            if t == None:
                t = Tags(name=tag)
                db.session.add(t)
            t.blogs.append(blog)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('writeBlog.html', legend="Create new post", title='Post', form=form)


@app.route('/blog/<int:blogid>/update', methods=['GET', 'POST'])
@login_required
def update_post(blogid):
    blog = Blogs.query.get_or_404(blogid)
    if blog.author != current_user:
        abort(403)
    form = BlogForm()
    if form.validate_on_submit():
        to_remove = blog.tags
        while to_remove:
            blog.tags.remove(to_remove[0])
            to_remove = blog.tags
        db.session.commit()
        tags = form.tags.data.split(' ')[:-1]
        for tag in tags:
            t = Tags.query.filter_by(name=tag).first()
            if t == None:
                t = Tags(name=tag)
                db.session.add(t)
            t.blogs.append(blog)
        blog.title = form.title.data
        blog.content = form.editordata.data
        db.session.commit()
        return redirect(url_for('blogpage', blogid=blogid))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.editordata.data = blog.content
        tags = blog.tags
    return render_template('writeBlog.html', legend='Update post', title='update', form=form, tags=tags)


@app.route('/blog/<int:blogid>/delete', methods = ['GET'])
@login_required
def delete_post(blogid):
    post = Blogs.query.get_or_404(blogid)
    if post.author == current_user:
        try:
            file_path = os.path.join(app.root_path, 'static/assets/thumbnails/', post.thumbnail)
            os.remove(file_path)
        except FileNotFoundError:
            pass
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        abort(403)


@app.route('/tag/<tagName>')
def search(tagName):
    tag = Tags.query.filter_by(name=tagName).first()
    blogs = tag.blogs
    return render_template('tagSearchResults.html', searchResult=blogs, tag=tag)


@app.route('/register', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        author = Authors(name=form.name.data, email=form.email.data,
                         password=bcrypt.generate_password_hash(form.password.data))
        db.session.add(author)
        db.session.commit()
        return redirect('author')
    return render_template('register.html', title='Register', form=form)


@app.route('/profile/<int:authorid>/', methods = ['GET'])
def profile(authorid):
    author = Authors.query.get_or_404(authorid)
    return render_template('author.html', author = author, title = 'Profile-'+author.name)


@app.route('/profile/<int:authorid>/edit', methods = ['GET', 'POST'])
@login_required
def edit_profile(authorid):
    author = Authors.query.get_or_404(authorid)
    if author == current_user:
        form = ProfileForm()
        if form.validate_on_submit():
            cleaned_data = bleach_tags(form.about_me.data)
            author.about = cleaned_data
            if form.profile_pic_encoded.data:
                profile_pic_name = save_file(form.profile_pic_encoded.data, 'static/assets/profile_pics')
                author.image_file = profile_pic_name
            db.session.commit()
            return redirect(url_for('profile', authorid = authorid))
        elif request.method == 'GET':
            form.about_me.data = author.about
            return render_template('edit_profile.html', title = 'Edit Profile', form = form)
    else:
        abort(403)
