from database.db import db
from flask import g
from flask_restful import Resource, reqparse
from src.Feedbacks.models import Feedback
from src.Feedbacks.serializers import FeedbackSchema
from src.User.model import UserModel
from src.middlewares.auth_middleware import token_required

feedbacks_schema = FeedbackSchema(many=True)

class FeedbackResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comment', type=str, help='Comment is required', required=True)
        self.parser.add_argument('rating', type=int, help='Rating is required', required=True)

    @token_required
    def post(self):
        args = self.parser.parse_args()
        current_user = g.current_user
        # Ensure the user exists before creating feedback
        user = UserModel.query.get_or_404(current_user.id)
        
        new_feedback = Feedback(
            comment=args['comment'],
            rating=args['rating'],
            user=user
        )

        db.session.add(new_feedback)
        db.session.commit()
        # Serialize the created feedback using the schema
        result = FeedbackSchema.dump(new_feedback)

        return {"data": result, 'message': 'Feedback submitted successfully'}, 201

class FeedbackListResource(Resource):
    @token_required
    def get(self):
        feedback_list = Feedback.query.all()

        # Serialize the list of feedbacks using the schema
        result = feedbacks_schema.dump(feedback_list)

        return {'feedback': result}, 200


class UserFeedbackListResource(Resource):
    @token_required
    def get(self):
        current_user = g.current_user
        feedback_list = Feedback.query.filter_by(user=current_user)

        # Serialize the list of feedbacks using the schema
        result = feedbacks_schema.dump(feedback_list)

        return {'feedback': result}, 200