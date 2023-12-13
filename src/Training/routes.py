from src.Training.views import QuestionResource, QuestionsResource, AnswerResource, AnswersResource, TestingResources, UserAnswerResource, UserResponsesResource, SaveUserAnswerResource

def training_routes(api):
    api.add_resource(QuestionResource, '/admin/question/<int:question_id>')
    api.add_resource(QuestionsResource, '/admin/questions')
    api.add_resource(AnswerResource, '/admin/answer/<int:answer_id>')
    api.add_resource(AnswersResource, '/admin/answers')
    api.add_resource(UserAnswerResource, '/api/check-answer')
    api.add_resource(UserResponsesResource, '/api/user-responses/<int:user_id>')
    api.add_resource(SaveUserAnswerResource, '/api/save-user-answer')
    api.add_resource(TestingResources, '/api/test')