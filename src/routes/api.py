from src.api.resources.auth import Register
from src.api.resources.pages.dashboard import Dashboard


def routes(api):
    api.add_resource(Register, '/signup')
    api.add_resource(Dashboard, '/dashboard')


def admin_routes(admin_api):
    pass
