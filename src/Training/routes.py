from src.Training.views import (
    CategoryResource, 
    CategoryListResource, 
    QuestionResource, 
    QuestionsResource, 
    AnswerResource, 
    AnswersResource, 
    TestingResources, 
    UserAnswerResource, 
    UserResponsesResource
)

def training_routes(api):
    api.add_resource(CategoryResource, '/admin/categories/<int:category_id>')
    api.add_resource(CategoryListResource, '/admin/categories')
    api.add_resource(QuestionResource, '/admin/question/<int:question_id>')
    api.add_resource(QuestionsResource, '/admin/questions')
    api.add_resource(AnswerResource, '/admin/answer/<int:answer_id>')
    api.add_resource(AnswersResource, '/admin/answers')
    api.add_resource(UserAnswerResource, '/save-user-answer')
    api.add_resource(UserResponsesResource, '/user-responses/<int:user_id>')
    api.add_resource(TestingResources, '/api/test')