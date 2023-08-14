from src.Dashboard.view import Dashboard, SummaryStatistics, UseCases
from src.Filters.view import Filters, MissingFilterKit, allowMissingPerc, \
    dimensionalityReductionOptions, normalizationOptions

def routes(api):
    api.add_resource(Dashboard, '/dashboard')
    api.add_resource(SummaryStatistics, '/get-summary-statistics')
    api.add_resource(Filters, '/filters')
    api.add_resource(MissingFilterKit, '/missing-filter-kit')
    api.add_resource(allowMissingPerc, '/allow-missing-perc-kit')
    api.add_resource(normalizationOptions, '/normalization-options-kit')
    api.add_resource(dimensionalityReductionOptions, '/dimensionality-reduction-options-kit')
    api.add_resource(UseCases, '/get-use-cases')