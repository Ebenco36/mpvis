from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from src.implementation.pages import Pages
from src.User.model import UserModel
from src.models.schemas.user import UserSchema, user_summary
import json
from flask import jsonify, request
from src.implementation.Helpers.helper import summaryStatisticsConverter
from src.Dashboard.data import stats_data
from src.implementation.graphs.helpers import Graph
from src.implementation.visualization import DataImport
from src.implementation.Helpers.machine_learning_al.sklearnML import MachineLearning
from src.implementation.Helpers.machine_learning_al.dimensionality_reduction import DimensionalityReduction
from src.implementation.data.columns.quantitative.quantitative import cell_columns, rcsb_entries
from src.implementation.data.columns.quantitative.quantitative_array import quantitative_array_column
from src.implementation.Helpers.machine_learning_al.normalization import Normalization
from src.implementation.data.columns.norminal import descriptors
from src.implementation.exceptions.AxisExceptions import AxisException
from src.implementation.Helpers.helper import find_dict_with_value_in_nested_data
from src.implementation.basic_plots import home_page_graph
from src.implementation.Helpers.helper import tableHeader
from src.middlewares.auth_middleware import token_required

user_schema = UserSchema()


class Dashboard(Resource):
    def __init__(self):
        data_import = DataImport()
        self.dataset = data_import.loadFile()
        self.pages = Pages(self.dataset)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('param', type=str, help='Sample parameter')

    # @staticmethod
    # @token_required
    def get(self):
        args = self.parser.parse_args()
        # Get the pagination parameters from the query string
        page = int(request.args.get('page', 1))
        conf = request.args.get('chart_conf', '{"color": "#a855f7", "opacity": 0.9}')
        conf = json.loads(conf)
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
        trend = home_page_graph(conf)
        default_display = [
            "Group", 'Taxonomic Domain', 'citation_country', 'citation_year'
        ]
        request_for_group = request.args.get('group_key', 'Taxonomic Domain')
        # Split the string on commas to create a list
        request_for_group_list = request_for_group.split(',')

        # merge array/list
        group_list = default_display + request_for_group_list

        # Convert the list to a set to get unique elements
        unique_group_list = list(set(group_list))

        group_graph_array = []

        for (key, graph) in enumerate(unique_group_list):
            group_graph, _ = self.pages.view_dashboard(graph, conf)
            obj = {
                "chart_obj": group_graph,
                "id": "graph" + str(key),
                "name": "graph " + str(key),
                "groups": key,
            }
            group_graph_array.append(obj)
        # Sorting the list based group size
        group_graph = sorted(group_graph.values(), key=lambda obj: len(obj))
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


class SummaryStatistics(Resource):

    def __init__(self):
        data_import = DataImport()
        self.dataset = data_import.loadFile()
        self.pages = Pages(self.dataset)

    # @token_required
    def get(self):
        check_which_page = request.args.get('stats-data', 'no_where')

        group_field_selection = request.args.get('field_selection', 'Species')

        parent_data, summary_search_filter_options, group_field_selection = summaryStatisticsConverter(group_field_selection)
        group_dict = find_dict_with_value_in_nested_data(stats_data(), group_field_selection)
        if (check_which_page == "stats-categories"):
            data = parent_data
        else:
            conf = request.args.get('chart_conf', '{"color": "#a855f7", "opacity": 0.9}')
            conf = json.loads(conf)
            group_graph, dataframe = self.pages.view_dashboard(group_field_selection, conf)
            merged_list = summary_search_filter_options
            sorted_frame = dataframe.sort_values(by='Values', ascending=False).to_dict('records')
            data = {
                "group_dict"    : group_dict,
                "search_object" : merged_list,
                "data"          : group_graph,
                "headers"       : tableHeader(dataframe.columns),
                "dataframe"     : sorted_frame,
                "search_key"    : group_field_selection,
                "status"        : 'success',
            }
        return jsonify(data)



class UseCases(Resource):
    def __init__(self):
        pass

    def get(self):
        cases = [
            {"value": "case_1", "name": "case 1", "desc": """
                Use Case 1: K-Means Clustering for Structural Similarity Analysis
                Objective: Perform clustering on enriched Mpstruct and PDB data to identify structurally similar protein conformations.
                <div>   
                    Steps:
                    <ul>
                        <li>Data Collection: Retrieve protein structural data from Mpstruct and PDB databases, including attributes like secondary structure elements, ligand binding sites, and torsion angles.</li>
                        <li>Feature Engineering: Preprocess and transform the data to create relevant features for clustering, such as combining torsion angles and secondary structure information.</li>
                        <li>K-Means Clustering: Apply K-Means clustering algorithm to group protein structures based on their structural features. Determine the optimal number of clusters using techniques like the elbow method.</li>
                        <li>Visualization: Visualize the clusters in a reduced dimension space using techniques like Principal Component Analysis (PCA).</li>
                        <li>Interpretation: Analyze the clusters to identify proteins with similar structural characteristics, potentially revealing insights into functional relationships.</li>
                    </ul>
                </div>
            """,
            "target": "Resolution"
            },
            {"value": "case_2", "name": "case 2", "desc": """
                Use Case 2: K-Means Clustering for Structural Similarity Analysis
                Objective: Perform clustering on enriched Mpstruct and PDB data to identify structurally similar protein conformations.
                <div>   
                    Steps:
                    <ul>
                        <li>Data Collection: Retrieve protein structural data from Mpstruct and PDB databases, including attributes like secondary structure elements, ligand binding sites, and torsion angles.</li>
                        <li>Feature Engineering: Preprocess and transform the data to create relevant features for clustering, such as combining torsion angles and secondary structure information.</li>
                        <li>K-Means Clustering: Apply K-Means clustering algorithm to group protein structures based on their structural features. Determine the optimal number of clusters using techniques like the elbow method.</li>
                        <li>Visualization: Visualize the clusters in a reduced dimension space using techniques like Principal Component Analysis (PCA).</li>
                        <li>Interpretation: Analyze the clusters to identify proteins with similar structural characteristics, potentially revealing insights into functional relationships.</li>
                    </ul>
                </div>
            """,
            "target": "Resolution"
            },
            {"value": "case_3", "name": "case 3", "desc": """
                Use Case 3: K-Means Clustering for Structural Similarity Analysis
                Objective: Perform clustering on enriched Mpstruct and PDB data to identify structurally similar protein conformations.
                <div>   
                    Steps:
                    <ul>
                        <li>Data Collection: Retrieve protein structural data from Mpstruct and PDB databases, including attributes like secondary structure elements, ligand binding sites, and torsion angles.</li>
                        <li>Feature Engineering: Preprocess and transform the data to create relevant features for clustering, such as combining torsion angles and secondary structure information.</li>
                        <li>K-Means Clustering: Apply K-Means clustering algorithm to group protein structures based on their structural features. Determine the optimal number of clusters using techniques like the elbow method.</li>
                        <li>Visualization: Visualize the clusters in a reduced dimension space using techniques like Principal Component Analysis (PCA).</li>
                        <li>Interpretation: Analyze the clusters to identify proteins with similar structural characteristics, potentially revealing insights into functional relationships.</li>
                    </ul>
                </div>
            """,
            "target": "Resolution"
            },
        ]

        return jsonify(cases)