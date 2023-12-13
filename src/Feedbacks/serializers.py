# serializers.py
from marshmallow import Schema, fields

class UserSchema(Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'name')  # Add other user-related fields

class FeedbackSchema(Schema):
    id = fields.Int()
    comment = fields.Str()
    rating = fields.Int()
    user = fields.Nested(UserSchema, only=('id', 'username', 'email', 'name'))
