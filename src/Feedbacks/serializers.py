# serializers.py
from marshmallow import Schema, fields

class UserSchema(Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'name')  # Add other user-related fields

class FeedbackSchema(Schema):
    id = fields.Int(dump_only=True)
    comment = fields.Str(required=True)
    responses = fields.Str(required=True)
    user_id = fields.Int(required=True)  # Add user_id field
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user = fields.Nested(UserSchema, only=('id',))

    def serialize(self, feedback):
        return {
            'id': feedback.id,
            'comment': feedback.comment,
            'responses': feedback.responses,
            'user': UserSchema().dump(feedback.user),
            'created_at': feedback.created_at,
            'updated_at': feedback.updated_at,
        }

class FeedbackOptionSchema(Schema):
    id = fields.Int()
    value = fields.Str()

class FeedbackQuestionSchema(Schema):
    id = fields.Int()
    question_text = fields.Str()
    options = fields.List(fields.Nested(FeedbackOptionSchema)) # fields.Nested(FeedbackOptionSchema, many=True)

class FeedbackQuestionWithAnswersSchema(Schema):
    id = fields.Int()
    question_text = fields.Str()
    answers = fields.List(fields.Nested(FeedbackOptionSchema))