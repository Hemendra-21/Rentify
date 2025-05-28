from flask_mail import Message
from app.main.extensions import mail
from threading import Thread 
from flask import current_app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

   
def send_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients, body=body)
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
