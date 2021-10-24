from flask_mail import Message
from blogApp import mail, app


def send_mail(recipients, sender, text_body, html_body):
    msg = Message(subject='StoryTell password reset mail',
                  recipients=recipients, sender=sender)
    msg.body = text_body
    msg.html = html_body
    print(recipients)
    print(sender)
    mail.send(msg)
    


