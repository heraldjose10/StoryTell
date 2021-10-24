from flask_mail import Message
from blogApp import mail
from threading import Thread
from flask import current_app


def asycn_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(recipients, sender, text_body, html_body):
    msg = Message(subject='StoryTell password reset mail',
                  recipients=recipients, sender=sender)
    msg.body = text_body
    msg.html = html_body
    Thread(target= asycn_mail, args=(current_app._get_current_object(), msg)).start()    


