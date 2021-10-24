from blogApp.email import send_mail
from flask import render_template, current_app


def send_pass_reset_mail(user):
    token = user.get_password_reset_token()
    send_mail(recipients=[user.email],
              sender=current_app.config['ADMINS'][0],
              text_body=render_template('email/password_reset_mail.txt', user=user, token=token),
              html_body=render_template('email/password_reset_mail.html', user=user, token=token))
