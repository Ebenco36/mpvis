from flask_mail import Mail, Message

class EmailService:
    def __init__(self, app=None):
        self.mail = Mail(app)

    def send_email(self, subject, sender, recipients, body):
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = body
        self.mail.send(msg)