from flask_restful import Resource, reqparse
from flask import jsonify, request
from src.implementation.Helpers.fields_helper import date_grouping_methods, \
    dimensionality_reduction_algorithms_helper_kit, graph_group_by_date, \
    graph_group_by_others, graph_options, graph_selection_categories_UI_kit, \
    graph_types_kit, grouping_aggregation_methods, machine_algorithms_helper_kit, \
    merge_graph_into_one_kit, multi_select_kit, normalization_algorithms_helper_kit, \
    quantification_fields_kit, missing_algorithms_helper_kit, perc_of_missing_value_kit, \
    dataSplitPercOption, PCAComponentsOption

from src.middlewares.auth_middleware import token_required

class Filters(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('param', type=str, help='Sample parameter')

    # @staticmethod
    # @token_required
    def get(self):
        selection_avenue_default, selection_type_default = graph_options()
        result = {
            'selection_avenue_default': selection_avenue_default,
            'selection_type_default': selection_type_default,
            'graph_types_kit': graph_types_kit(),
            'machine_algorithms_helper_kit': machine_algorithms_helper_kit(),
            'dimensionality_reduction_algorithms_helper_kit': dimensionality_reduction_algorithms_helper_kit(),
            'normalization_algorithms_helper_kit': normalization_algorithms_helper_kit(),
            'graph_selection_categories_UI_kit': graph_selection_categories_UI_kit(),
            'graph_group_by_date': graph_group_by_date(),
            'graph_group_by_others': graph_group_by_others(),
            'date_grouping_methods': date_grouping_methods(),
            'grouping_aggregation_methods': grouping_aggregation_methods(),
            'multi_select_kit': multi_select_kit(),
            'quantification_fields_kit': quantification_fields_kit(),
            'merge_graph_into_one_kit': merge_graph_into_one_kit(),
        }
        # Return the result as JSON using Flask's jsonify function
        return jsonify(result)


class MissingFilterKit(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('param', type=str, help='Sample parameter')

    # @staticmethod
    # @token_required
    def get(self):
        result = missing_algorithms_helper_kit()
        # Return the result as JSON using Flask's jsonify function
        return jsonify(result)
    

class allowMissingPerc(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('param', type=str, help='Sample parameter')

    # @staticmethod
    # @token_required
    def get(self):
        result = perc_of_missing_value_kit()
        # Return the result as JSON using Flask's jsonify function
        return jsonify(result)
    

class normalizationOptions(Resource):
    def __init__(self):
        pass
    # @staticmethod
    # @token_required
    def get(self):
        result = normalization_algorithms_helper_kit()
        # Return the result as JSON using Flask's jsonify function
        return jsonify(result)
    


class dimensionalityReductionOptions(Resource):
    def __init__(self):
        pass
    # @staticmethod
    # @token_required
    def get(self):
        result = dimensionality_reduction_algorithms_helper_kit()
        # Return the result as JSON using Flask's jsonify function
        return jsonify(result)
    


class dataSplitPercOptions(Resource):
    def __init__(self):
        pass
    # @staticmethod
    # @token_required
    def get(self):
        result = dataSplitPercOption()
        # Return the result as JSON using Flask's jsonify function
        return jsonify(result)
    

class PCAComponentsOptions(Resource):
    def __init__(self):
        pass
    # @staticmethod
    # @token_required
    def get(self):
        features = request.args.get('n_features', 2)
        result = PCAComponentsOption(features)
        # Return the result as JSON using Flask's jsonify function
        return jsonify(result)