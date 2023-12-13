from src.MP.views import DataResource, CategoricalDataResource

def MP_routes(api):
    api.add_resource(DataResource, '/data-view')
    api.add_resource(CategoricalDataResource, '/data-view-categorical')