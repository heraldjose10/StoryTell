from flask import render_template, redirect, request, url_for, abort, current_app
from blogApp.posts.forms import BlogForm
from blogApp.models import Tags, Blogs
from flask_login import login_required, current_user
from blogApp import db
from blogApp.utils import bleach_tags, save_file
from blogApp.posts import bp
import os


@bp.route('/blog/<blogid>')
def blogpage(blogid):
    blog = Blogs.query.get(int(blogid))
    return render_template('blogpage.html', blog=blog)


@bp.route('/create_blog', methods=['Get', 'POST'])
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
        return redirect(url_for('core.index'))
    return render_template('writeBlog.html', legend="Create new post", title='Post', form=form)


@bp.route('/blog/<int:blogid>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.blogpage', blogid=blogid))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.editordata.data = blog.content
        tags = blog.tags
    return render_template('writeBlog.html', legend='Update post', title='update', form=form, tags=tags)


@bp.route('/blog/<int:blogid>/delete', methods = ['GET'])
@login_required
def delete_post(blogid):
    post = Blogs.query.get_or_404(blogid)
    if post.author == current_user:
        try:
            file_path = os.path.join(current_app.root_path, 'static/assets/thumbnails/', post.thumbnail)
            os.remove(file_path)
        except FileNotFoundError:
            pass
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('core.index'))
    else:
        abort(403)
