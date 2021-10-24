from flask import render_template, request, redirect, url_for, abort
from blogApp.profile.forms import ProfileForm
from blogApp.models import Authors
from flask_login import login_required, current_user
from blogApp.utils import save_file, bleach_tags
from blogApp import db
from blogApp.profile import bp


@bp.route('/profile/<int:authorid>/', methods = ['GET'])
def profile(authorid):
    author = Authors.query.get_or_404(authorid)
    return render_template('author.html', author = author, title = 'Profile-'+author.name)


@bp.route('/profile/<int:authorid>/edit', methods = ['GET', 'POST'])
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
            return redirect(url_for('profile.profile', authorid = authorid))
        elif request.method == 'GET':
            form.about_me.data = author.about
            return render_template('edit_profile.html', title = 'Edit Profile', form = form)
    else:
        abort(403)
