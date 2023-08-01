from src.Dashboard.view import Dashboard, SampleChart


def routes(api):
    api.add_resource(Dashboard, '/dashboard')
    api.add_resource(SampleChart, '/get_chart_data')