# serializers.py
from marshmallow import Schema, fields, validates, ValidationError
from src.Training.models import Category
from flask_marshmallow import Marshmallow
from flask import Flask, current_app

app = Flask(__name__)
with app.app_context():
    ma = Marshmallow(app)



class AnswerSchema(Schema):
    id = fields.Int()
    text = fields.Str()
    is_correct = fields.Bool()
    question_id = fields.Int()
    created_at = fields.Date()
    updated_at = fields.Date()
    
    
class QuestionSchema(Schema):
    id = fields.Int()
    text = fields.Str()
    category_id = fields.Int()
    created_at = fields.Date()
    updated_at = fields.Date()
    answers = fields.Nested(
        AnswerSchema, 
        many=True,  
        data_key='options',
        only=('id', 'text', 'is_correct', 'question_id')
    )

    @validates('answers')
    def validate_answers(self, value):
        # Ensure at least one answer is marked as correct
        correct_answers = [answer for answer in value if answer.get('is_correct')]
        if not correct_answers:
            raise ValidationError('At least one answer must be marked as correct.')



class CategorySchema(ma.SQLAlchemyAutoSchema):
    questions = ma.Nested(QuestionSchema, many=True)
    class Meta:
        model = Category
     