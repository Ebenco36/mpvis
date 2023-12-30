# resources.py

import uuid
from flask import g, request
from flask_restful import Resource, reqparse
from src.Training.models import Category
from src.Training.serializers import QuestionSchema, CategorySchema
from sqlalchemy.orm import joinedload
from src.Training.services import CategoryService, QuestionService, AnswerService, get_records_on_method
from src.middlewares.auth_middleware import token_required

question_parser = reqparse.RequestParser()
question_parser.add_argument('text', type=str, help='Text of the question')

answer_parser = reqparse.RequestParser()
answer_parser.add_argument('text', type=str, help='Text of the answer')
answer_parser.add_argument('question_id', type=int, help='question id')
answer_parser.add_argument('is_correct', type=bool, help='Is the answer correct')


class CategoryResource(Resource):
    @token_required
    def get(self, category_id):
        category = CategoryService.get_category(category_id)
        category_schema = CategorySchema()
        return category_schema.dump(category)
    
    @token_required
    def put(self, category_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
        parser.add_argument('description', type=str, required=False)
        args = parser.parse_args()

        # Check if the category with the given ID exists
        existing_category = CategoryService.get_category(category_id)
        if not existing_category:
            return {"message": "Category not found"}, 404

        # Update the category
        updated_category = CategoryService.update_category(category_id, args['name'], args['description'])

        if updated_category:
            category_schema = CategorySchema()  # Replace with your actual CategorySchema
            return category_schema.dump(updated_category)
        else:
            return {"message": "Cannot update category. Another category with the same name may exist."}, 400
        
    @token_required
    def delete(self, category_id):
        deleted = CategoryService.delete_category(category_id)
        if deleted:
            return {"message": f"Category deleted successfully."}
        else:
            return {"message": "Cannot delete category. Questions are attached."}, 400

class CategoryListResource(Resource):
    @token_required
    def get(self):
        categories = CategoryService.get_all_categories()
        category_schema = CategorySchema(many=True)
        return category_schema.dump(categories)

    @token_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
        parser.add_argument('description', type=str, required=True, help='Description cannot be blank')
        args = parser.parse_args()

        new_category = CategoryService.create_category(args['name'], args['description'])
        if new_category:
            category_schema = CategorySchema()
            return category_schema.dump(new_category), 201
        else:
            return {"message": "Category with this name already exists."}, 400


class QuestionResource(Resource):
    @token_required
    def get(self, question_id):
        question = QuestionService.get_question_by_id(question_id)
        question_schema = QuestionSchema()
        return question_schema.dump(question), 200
    
    @token_required
    def put(self, question_id):
        question_parser.add_argument('text', type=str, required=True, help='Question text')
        question_parser.add_argument('category_id', type=str, required=True, help='Question category')
        args = question_parser.parse_args()
        question = QuestionService.get_question_by_id(question_id)
        if question:
            category = Category.query.get_or_404(args['category_id'])
            QuestionService.update_question(question, args['text'], category)
            return {'message': 'Question updated successfully'}
        return {'message': 'Question not found'}, 404

    @token_required
    def delete(self, question_id):
        question = QuestionService.get_question_by_id(question_id)
        if question:
            QuestionService.delete_question(question)
            return {'message': 'Question deleted successfully'}
        return {'message': 'Question not found'}, 404

class QuestionsResource(Resource):
    
    @token_required
    def get(self):
        questions = QuestionService.get_all_questions()
        question_schema = QuestionSchema(many=True)
        return question_schema.dump(questions), 200

    @token_required
    def post(self):
        question_parser.add_argument('text', type=str, required=True, help='Question text')
        question_parser.add_argument('category_id', type=str, required=True, help='Question category')
        args = question_parser.parse_args()
        category = Category.query.get_or_404(args['category_id'])
        question = QuestionService.create_question(args['text'], category)
        return {
            'id': question.id, 
            'text': question.text, 
            'category_id': question.category_id,
            'created_at': question.created_at.isoformat(),
            'created_at': question.updated_at.isoformat(),
            'options': question.answers
        }, 201

class AnswerResource(Resource):
    
    @token_required
    def get(self, answer_id):
        answer = AnswerService.get_answer_by_id(answer_id)
        if(answer):
            return {
                    'id': answer.id, 
                    'text': answer.text, 
                    'is_correct': answer.is_correct,
                    'question_id': answer.question_id,
                    'created_at': answer.created_at.isoformat(),
                    'created_at': answer.updated_at.isoformat(),
            }, 200
        else: 
            return {'message': 'Answer not found'}, 404

    @token_required
    def put(self, answer_id):
        args = answer_parser.parse_args()
        answer = AnswerService.get_answer_by_id(answer_id)
        if answer:
            AnswerService.update_answer(answer, args['text'], args['is_correct'])
            return {'message': 'Answer updated successfully'}
        return {'message': 'Answer not found'}, 404

    @token_required
    def delete(self, answer_id):
        answer = AnswerService.get_answer_by_id(answer_id)
        if answer:
            AnswerService.delete_answer(answer)
            return {'message': 'Answer deleted successfully'}
        return {'message': 'Answer not found'}, 404

class AnswersResource(Resource):
    @token_required
    def get(self):
        answers = AnswerService.get_all_answers()
        return [{'id': a.id, 'text': a.text, 'is_correct': a.is_correct, 'question_id': a.question_id} for a in answers]

    @token_required
    def post(self):
        args = answer_parser.parse_args()
        answer = AnswerService.create_answer(args['text'], args['question_id'], args['is_correct'])
        return {'id': answer.id, 'text': answer.text, 'is_correct': answer.is_correct, 'question_id': answer.question_id}, 201


class UserAnswerResource(Resource):
    @token_required
    def post(self):
        data = request.get_json()
        session_id = request.headers.get('X-Session-ID') or str(uuid.uuid4())
        current_user = g.current_user
        response = AnswerService.check_user_response(current_user.id, session_id, data)
        return response
    
class UserResponsesResource(Resource):
    @token_required
    def get(self, user_id):
        user_responses = AnswerService.get_user_responses(user_id)
        return [{'question_id': ur.question_id, 'answer_id': ur.answer_id} for ur in user_responses]


class TestingResources(Resource):
    def get(self):
        data = get_records_on_method()
        return data