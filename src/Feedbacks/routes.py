from src.Feedbacks.views import FeedbackResource, FeedbackListResource, UserFeedbackListResource

def feedback_routes(api):
    api.add_resource(FeedbackResource, '/feedback')
    api.add_resource(UserFeedbackListResource, '/my-feedback')
    api.add_resource(FeedbackListResource, '/feedback/all')