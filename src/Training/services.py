# services.py

from src.Training.models import db, Question, Answer, UserResponse
from src.Dashboard.services import get_table_as_dataframe
from src.MP.model import MembraneProteinData

class QuestionService:
    @staticmethod
    def create_question(text):
        question = Question(text=text)
        db.session.add(question)
        db.session.commit()
        return question

    @staticmethod
    def get_all_questions():
        return Question.query.all()

    @staticmethod
    def get_question_by_id(question_id):
        return Question.query.get(question_id)

    @staticmethod
    def update_question(question, text):
        question.text = text
        db.session.commit()

    @staticmethod
    def delete_question(question):
        db.session.delete(question)
        db.session.commit()

class AnswerService:
    @staticmethod
    def create_answer(text, question_id, is_correct=False):
        answer = Answer(text=text, question_id=question_id, is_correct=is_correct)
        db.session.add(answer)
        db.session.commit()
        return answer

    @staticmethod
    def get_all_answers():
        return Answer.query.all()

    @staticmethod
    def get_answer_by_id(answer_id):
        return Answer.query.get(answer_id)

    @staticmethod
    def update_answer(answer, text, is_correct):
        answer.text = text
        answer.is_correct = is_correct
        db.session.commit()

    @staticmethod
    def delete_answer(answer):
        db.session.delete(answer)
        db.session.commit()

    
    @staticmethod
    def get_user_responses(user_id):
        return UserResponse.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_user_response(user_id, question_id, answer_id):
        user_response = UserResponse(user_id=user_id, question_id=question_id, answer_id=answer_id)
        db.session.add(user_response)
        db.session.commit()
        return user_response
    
    
    @staticmethod
    def check_user_response(user_id, question_id, answer_id):
        # Get the correct answer for the question
        correct_answer = Answer.query.filter_by(question_id=question_id, is_correct=True).first()

        # Check if the user's answer is correct
        is_correct = answer_id == correct_answer.id

        # Record the user's response
        user_response = UserResponse(user_id=user_id, question_id=question_id, answer_id=answer_id, is_correct=is_correct)
        db.session.add(user_response)
        db.session.commit()

        return {'is_correct': is_correct, 'correct_answer_id': correct_answer.id}
    
    
    
    """
        implement classes based on the different methods
        There is a lot here..
        Current methods are: X-ray, 
    """
        
def get_records_on_method():
    query = MembraneProteinData.query.filter_by(rcsentinfo_experimental_method="NMR")
    sql_statement = str(query.statement)
    
    # Example usage with filter
    filter_column = 'rcsentinfo_experimental_method'
    filter_value = 'NMR'
    result_df = get_table_as_dataframe("membrane_proteins", filter_column, filter_value)
    return result_df

    