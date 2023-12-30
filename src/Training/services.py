# services.py

from sqlalchemy.exc import IntegrityError
from src.Training.models import db, Category, Question, Answer, UserResponse
from src.Dashboard.services import get_table_as_dataframe
from src.MP.model import MembraneProteinData
from sqlalchemy.orm import joinedload
from datetime import datetime


class CategoryService:
    @staticmethod
    def get_category(category_id):
        return Category.query.get_or_404(category_id)

    @staticmethod
    def delete_category(category_id):
        category = Category.query.get_or_404(category_id)
        if not category.questions:
            db.session.delete(category)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_categories():
        # return Category.query.options(joinedload(Category.questions)).all()
        return (
            Category.query
            .options(
                joinedload(Category.questions)
                .joinedload(Question.answers)
            )
            .filter(Category.questions.any(Question.answers.any()))
            .all()
        )

    @staticmethod
    def create_category(name, description):
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            return None
        new_category = Category(name=name, description=description)
        db.session.add(new_category)
        db.session.commit()
        return new_category
    

    @staticmethod
    def update_category(category_id, name, description):
        category = Category.query.get_or_404(category_id)

        # Check if a category with the new name already exists
        existing_category = Category.query.filter(
            Category.id != category_id,
            Category.name == name,
        ).first()

        if existing_category:
            return None  # Another category with the same name already exists

        category.name = name
        category.description = description

        try:
            db.session.commit()
            return category
        except IntegrityError:
            db.session.rollback()
            return None  # IntegrityError indicates a unique constraint violation

    
class QuestionService:
    @staticmethod
    def create_question(text, category):
        question = Question(text=text, category=category)
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
    def update_question(question, text, category):
        question.text = text
        question.category = category
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
    def check_user_response(user_id, session_id, data_list):
        # Create records in the UserResponse model
        
        for data_item in data_list:
            # Check if a response already exists for the user and question
            existing_response = UserResponse.query.filter_by(
                session_id=session_id,
                user_id=user_id,
                question_id=data_item['question_id']
            ).first()

            if existing_response:
                # Update the existing response
                existing_response.answer_id = data_item['id']
                existing_response.is_correct = data_item['is_correct']
                existing_response.updated_at = datetime.utcnow()
            else:
                # Create a new response
                user_response = UserResponse(
                    session_id=session_id,
                    user_id=user_id,
                    question_id=data_item['question_id'],
                    answer_id=data_item['id'],
                    is_correct=data_item['is_correct']
                )
                db.session.add(user_response)

        # Commit the changes
        db.session.commit()

        return {'message': "Added or updated user responses"}
    
    
    
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

    