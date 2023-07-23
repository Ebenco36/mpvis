from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from src.models.user import UserModel
from src.models.schemas.user import UserSchema, user_summary
import pandas as pd
import altair as alt
import random
import json
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

user_schema = UserSchema()


class Dashboard(Resource):
    def __init__(self):
        data_import = DataImport()
        self.dataset = data_import.loadFile()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('param', type=str, help='Sample parameter')

    # @staticmethod
    def get(self):
        args = self.parser.parse_args()
        return self.dataset
        return {'message': 'Request object displayed successfully', 'request_args': args}, 200
    
    @staticmethod
    # @UserSchema.validate_fields(location=('json',))
    def post(self, args):
        return {
            'success': True,
        }, 201

