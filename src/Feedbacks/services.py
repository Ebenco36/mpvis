from marshmallow import ValidationError
from database.db import db
from src.Feedbacks.models import Feedback, FeedbackQuestion, FeedbackOption
from src.Feedbacks.serializers import FeedbackQuestionSchema, FeedbackSchema


# Service to handle CRUD operations for feedback questions
class FeedbackService:
    @staticmethod
    def get_all_questions():
        return [question.to_dict() for question in FeedbackQuestion.query.all()]

    @staticmethod
    def get_question_by_id(question_id):
        question = FeedbackQuestion.query.get(question_id)
        return question.to_dict() if question else None

    @staticmethod
    def add_question(question_text, options):
        new_question = FeedbackQuestion(question_text=question_text)
        for option_value in options:
            new_option = FeedbackOption(value=option_value)
            new_question.options.append(new_option)
        db.session.add(new_question)
        db.session.commit()
        return new_question.to_dict()

    @staticmethod
    def update_question(question_id, new_options):
        question = FeedbackQuestion.query.get(question_id)
        if question:
            # Delete existing options
            FeedbackOption.query.filter_by(question_id=question_id).delete()

            # Add new options
            for option_value in new_options:
                new_option = FeedbackOption(value=option_value)
                question.options.append(new_option)

            db.session.commit()
            return question.to_dict()
        return None

    @staticmethod
    def delete_question(question_id):
        question = FeedbackQuestion.query.get(question_id)
        if question:
            db.session.delete(question)
            db.session.commit()
            return {"message": f"Question '{question_id}' deleted successfully"}
        return {"error": "Question not found"}


    
    @staticmethod
    def update_or_create_questions(data):
        results = []

        for item in data:
            question_text = item.get("question_text")
            options = item.get("options")

            if not question_text or not options:
                results.append({"error": "Invalid data format"})
                continue

            try:
                validated_data = FeedbackQuestionSchema().load(item)
            except ValidationError as e:
                results.append({"error": f"Validation error for question '{question_text}': {e.messages}"})
                continue

            existing_question = FeedbackQuestion.query.filter_by(question_text=question_text).first()

            if existing_question:
                # Update existing question
                existing_question.options = []  # Clear existing options

                for option_data in validated_data['options']:
                    new_option = FeedbackOption(value=option_data['value'], question_id=existing_question.id)
                    existing_question.options.append(new_option)

                db.session.commit()

                results.append({"message": f"Question '{question_text}' updated successfully"})
            else:
                # Create a new question
                new_question = FeedbackQuestion(question_text=question_text)

                for option_data in validated_data['options']:
                    new_option = FeedbackOption(value=option_data['value'], question_id=new_question.id)
                    new_question.options.append(new_option)

                db.session.add(new_question)
                db.session.commit()

                results.append({"message": f"Question '{question_text}' created successfully"})

        return results


class UserFeedbackService:
    feedback_schema = FeedbackSchema()

    @staticmethod
    def get_user_feedbacks(user_id):
        feedbacks = Feedback.query.filter_by(user_id=user_id).all()
        formatted_feedbacks = [UserFeedbackService.feedback_schema.dump(feedback) for feedback in feedbacks]
        return formatted_feedbacks

    @staticmethod
    def store_user_feedback(args):
        
        new_feedback = Feedback(user_id=args['user_id'], comment=args['comment'], responses=args['responses'])
        db.session.add(new_feedback)
        db.session.commit()
        
        # Serialize and return the newly created feedback using the schema
        return UserFeedbackService.feedback_schema.dump(new_feedback)