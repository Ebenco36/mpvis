from src.Dashboard.view import Dashboard, SummaryStatistics, UseCases, MembraneProteinList
from src.Filters.view import Filters, MissingFilterKit, allowMissingPerc, \
    dimensionalityReductionOptions, normalizationOptions, dataSplitPercOptions, \
    PCAComponentsOptions, MachineLearningOptions, GraphOptions, trainAndTestSplitOptions

def routes(api):
    api.add_resource(Dashboard, '/dashboard')
    api.add_resource(MembraneProteinList, '/data-list')
    api.add_resource(SummaryStatistics, '/get-summary-statistics')
    api.add_resource(Filters, '/filters')
    api.add_resource(MissingFilterKit, '/missing-filter-kit')
    api.add_resource(allowMissingPerc, '/allow-missing-perc-kit')
    api.add_resource(dataSplitPercOptions, '/data-split-perc-options-kit')
    api.add_resource(PCAComponentsOptions, '/PCA-components-options-kit')
    api.add_resource(normalizationOptions, '/normalization-options-kit')
    api.add_resource(dimensionalityReductionOptions, '/dimensionality-reduction-options-kit')
    api.add_resource(MachineLearningOptions, '/machine-learning-options-kit')
    api.add_resource(trainAndTestSplitOptions, '/train-and-test-split-options-kit')
    api.add_resource(GraphOptions, '/graph-options-kit')
    api.add_resource(UseCases, '/get-use-cases')