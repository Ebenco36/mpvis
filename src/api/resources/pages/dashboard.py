from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from src.implementation.pages import Pages
from src.models.user import UserModel
from src.models.schemas.user import UserSchema, user_summary
import pandas as pd
import altair as alt
import random
import json
from flask import jsonify, request
from src.implementation.Helpers.helper import extract_function_names
from src.implementation.graphs.helpers import Graph
from src.implementation.visualization import DataImport
from src.implementation.Helpers.machine_learning_al.sklearnML import MachineLearning
from src.implementation.Helpers.machine_learning_al.dimensionality_reduction import DimensionalityReduction
from src.implementation.data.columns.quantitative.quantitative import cell_columns, rcsb_entries
from src.implementation.data.columns.quantitative.quantitative_array import quantitative_array_column
from src.implementation.Helpers.machine_learning_al.normalization import Normalization
from src.implementation.data.columns.norminal import descriptors
from src.implementation.exceptions.AxisExceptions import AxisException
from src.implementation.Helpers.helper import parser_change_dot_to_underscore
from src.implementation.basic_plots import home_page_graph
from vega_datasets import data


user_schema = UserSchema()


class Dashboard(Resource):
    def __init__(self):
        data_import = DataImport()
        self.dataset = data_import.loadFile()
        self.pages = Pages(self.dataset)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('param', type=str, help='Sample parameter')

    # @staticmethod
    def get(self):
        args = self.parser.parse_args()
        # Get the pagination parameters from the query string
        page = int(request.args.get('page', 1))
        records_per_page = int(request.args.get('records_per_page', 10))

        # Calculate the start and end index for slicing the DataFrame
        start_idx = (page - 1) * records_per_page
        end_idx = start_idx + records_per_page

        # Slice the DataFrame based on the pagination parameters
        paginated_df = self.dataset[start_idx:end_idx].fillna("").to_dict('records')
        # Generate the DataFrame summary statistics
        df_summary = self.dataset.describe(include='all').fillna("").to_dict()
        # Combine the paginated data and the summary statistics into a single dictionary
        rows, columns = self.dataset.shape
        trend = home_page_graph()
        default_display = [
            'Species', 'Taxonomic Domain', 'Resolution', 'citation_country', 'citation_year'
        ]
        request_for_group = request.args.get('group_key', 'Taxonomic Domain')
        # Split the string on commas to create a list
        request_for_group_list = request_for_group.split(',')

        # merge array/list
        group_list = default_display + request_for_group_list

        # Convert the list to a set to get unique elements
        unique_group_list = list(set(group_list))

        group_graph_array = []

        for graph in unique_group_list:
            group_graph = self.pages.view_dashboard(graph)
            group_graph_array.append(group_graph)

        result = {
            'rows': rows,
            'columns': columns,
            'summary': df_summary,
            'data': paginated_df,
            'group_graph_array': group_graph_array,
            'trend': trend
        }

        # Return the result as JSON using Flask's jsonify function
        return jsonify(result)
    
    @staticmethod
    # @UserSchema.validate_fields(location=('json',))
    def post(self, args):
        return {
            'success': True,
        }, 201


class SampleChart(Resource):
    def get(self):
        source = data.cars()

        chart = alt.Chart(source).mark_point().encode(
            x='Horsepower',
            y='Miles_per_Gallon',
            color='Origin',
        )

        chart_data = chart.to_dict()
        return chart_data