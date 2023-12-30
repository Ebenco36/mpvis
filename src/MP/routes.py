from src.MP.views import DataResource, UsupervisedResource, DataFilterResource

def MP_routes(api):
    api.add_resource(DataResource, '/data-view')
    api.add_resource(DataFilterResource, '/data-view-filters')
    api.add_resource(UsupervisedResource, '/data-view-ML')