import datetime
from database.db import db
from src.User.model import UserModel


class FeedbackOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('feedback_question.id'), nullable=False)


class FeedbackQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    options = db.relationship('FeedbackOption', backref='feedback_question', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "question_text": self.question_text,
            "options": [option.value for option in self.options]
        }

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    responses = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    user = db.relationship(UserModel, backref='feedbacks')
