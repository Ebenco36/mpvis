from src.UOT.views import UOT

def UOT_routes(api):
    api.add_resource(UOT, '/UOT')