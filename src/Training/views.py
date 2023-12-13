# resources.py

from flask_restful import Resource, reqparse
from src.Training.services import QuestionService, AnswerService, get_records_on_method

question_parser = reqparse.RequestParser()
question_parser.add_argument('text', type=str, help='Text of the question')

answer_parser = reqparse.RequestParser()
answer_parser.add_argument('text', type=str, help='Text of the answer')
answer_parser.add_argument('question_id', type=int, help='question id')
answer_parser.add_argument('is_correct', type=bool, help='Is the answer correct')

class QuestionResource(Resource):
    def get(self, question_id):
        question = QuestionService.get_question_by_id(question_id)
        if(question):
            return {
                    'id': question.id, 
                    'text': question.text, 
                    'created_at': question.created_at.isoformat(),
                    'options': question.answers
            }, 200
        else: 
            return {'message': 'Question not found'}, 404

    def put(self, question_id):
        args = question_parser.parse_args()
        question = QuestionService.get_question_by_id(question_id)
        if question:
            QuestionService.update_question(question, args['text'])
            return {'message': 'Question updated successfully'}
        return {'message': 'Question not found'}, 404

    def delete(self, question_id):
        question = QuestionService.get_question_by_id(question_id)
        if question:
            QuestionService.delete_question(question)
            return {'message': 'Question deleted successfully'}
        return {'message': 'Question not found'}, 404

class QuestionsResource(Resource):
    def get(self):
        questions = QuestionService.get_all_questions()
        return { 
            "data": [{
                'id': q.id, 
                'text': q.text, 
                'created_at': q.created_at.isoformat(),
                'options': q.answers
            } for q in questions], 
            "message" : "Fetched questions successfully."
        }

    def post(self):
        args = question_parser.parse_args()
        question = QuestionService.create_question(args['text'])
        return {
            'id': question.id, 
            'text': question.text, 
            'created_at': question.created_at.isoformat(),
            'options': question.answers
        }, 201

class AnswerResource(Resource):
    def get(self, answer_id):
        answer = AnswerService.get_answer_by_id(answer_id)
        if(answer):
            return {
                    'id': answer.id, 
                    'text': answer.text, 
                    'is_correct': answer.is_correct,
                    'question_id': answer.question_id
            }, 200
        else: 
            return {'message': 'Answer not found'}, 404

    def put(self, answer_id):
        args = answer_parser.parse_args()
        answer = AnswerService.get_answer_by_id(answer_id)
        if answer:
            AnswerService.update_answer(answer, args['text'], args['is_correct'])
            return {'message': 'Answer updated successfully'}
        return {'message': 'Answer not found'}, 404

    def delete(self, answer_id):
        answer = AnswerService.get_answer_by_id(answer_id)
        if answer:
            AnswerService.delete_answer(answer)
            return {'message': 'Answer deleted successfully'}
        return {'message': 'Answer not found'}, 404

class AnswersResource(Resource):
    def get(self):
        answers = AnswerService.get_all_answers()
        return [{'id': a.id, 'text': a.text, 'is_correct': a.is_correct, 'question_id': a.question_id} for a in answers]

    def post(self):
        args = answer_parser.parse_args()
        answer = AnswerService.create_answer(args['text'], args['question_id'], args['is_correct'])
        return {'id': answer.id, 'text': answer.text, 'is_correct': answer.is_correct, 'question_id': answer.question_id}, 201


class UserAnswerResource(Resource):
    def post(self):
        args = answer_parser.parse_args()
        response = AnswerService.check_user_response(args['user_id'], args['question_id'], args['answer_id'])
        return response
    
class SaveUserAnswerResource(Resource):
    def post(self):
        args = answer_parser.parse_args()
        answer = AnswerService.create_answer(args['text'], args['question_id'], args['is_correct'])
        return {'id': answer.id, 'text': answer.text, 'is_correct': answer.is_correct, 'question_id': answer.question_id}, 201
    
    
class UserResponsesResource(Resource):
    def get(self, user_id):
        user_responses = AnswerService.get_user_responses(user_id)
        return [{'question_id': ur.question_id, 'answer_id': ur.answer_id} for ur in user_responses]


class TestingResources(Resource):
    def get(self):
        data = get_records_on_method()
        print(data.columns)
        return data