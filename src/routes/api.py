from src.api.resources.auth import Register
from src.api.resources.pages.dashboard import Dashboard, SampleChart


def routes(api):
    api.add_resource(Register, '/signup')
    api.add_resource(Dashboard, '/dashboard')
    api.add_resource(SampleChart, '/get_chart_data')


def admin_routes(admin_api):
    pass
