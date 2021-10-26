from flask_mail import Message
from blogApp import mail
from threading import Thread
from flask import current_app


def asycn_mail(app, msg):
    """Function for sending mails asynchronously

    Parameters
    ----------
    app : app object
    msg : Message object
    """
    with app.app_context():
        mail.send(msg)


def send_mail(recipients, sender, text_body, html_body):
    """Function to send mail

    Parameters
    ----------
    recipients : list of users to which mail to be send
    sender : str email id of sender
    text_body : template of body in txt format
    html_body : template of body in HTML format
    """
    msg = Message(subject='StoryTell password reset mail',
                  recipients=recipients, sender=sender)
    msg.body = text_body
    msg.html = html_body
    # create a seperate thread and send mail using that thread
    Thread(target=asycn_mail, args=(
        current_app._get_current_object(), msg)).start()
