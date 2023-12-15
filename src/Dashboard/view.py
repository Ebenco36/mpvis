from flask_restful import Resource, reqparse
from src.Dashboard.services import get_items, get_table_as_dataframe
from src.services.pages import Pages
import json
from flask import jsonify, request
from src.services.Helpers.helper import summaryStatisticsConverter
from src.Dashboard.data import stats_data
from src.services.graphs.helpers import Graph
from src.services.visualization import DataImport
from src.services.Helpers.machine_learning_al.UnsupervisedMachineLearning import MachineLearning
from src.services.Helpers.machine_learning_al.dimensionality_reduction import DimensionalityReduction
from src.services.data.columns.quantitative.quantitative import cell_columns, rcsb_entries
from src.services.data.columns.quantitative.quantitative_array import quantitative_array_column
from src.services.Helpers.machine_learning_al.normalization import Normalization
from src.services.data.columns.norminal import descriptors
from src.services.exceptions.AxisExceptions import AxisException
from src.services.Helpers.helper import find_dict_with_value_in_nested_data
from src.services.basic_plots import home_page_graph, data_flow
from src.services.Helpers.helper import tableHeader
from src.middlewares.auth_middleware import token_required

class Dashboard(Resource):
    def __init__(self):
        pass

    # @staticmethod
    @token_required
    def get(self):
        
        # Get the DataFrame directly
        table_df = get_table_as_dataframe("membrane_proteins")
        pages = Pages(table_df)
        data = get_items(request)
        
        conf = request.args.get('chart_conf', '{"color": "#005EB8", "opacity": 0.9}')
        conf = json.loads(conf)
        # trend = home_page_graph(conf)
        trend = data_flow(table_df)
        default_display = [
            "group", 'taxonomic_domain', 'citation_country'
        ]
        request_for_group = request.args.get('group_key', 'taxonomic_domain')
        # Split the string on commas to create a list
        request_for_group_list = request_for_group.split(',')

        # merge array/list
        group_list = default_display + request_for_group_list

        # Convert the list to a set to get unique elements
        unique_group_list = list(set(group_list))

        group_graph_array = []

        for (key, graph) in enumerate(unique_group_list):
            group_graph, _ = pages.view_dashboard(graph, conf)
            obj = {
                "chart_obj": group_graph,
                "id": "graph" + str(key),
                "name": "graph " + str(key),
                "groups": graph,
            }
            
            group_graph_array.append(obj)
        # Sorting the list based group size
        # group_graph = sorted(group_graph.values(), key=lambda obj: obj)
        result = {
            'data': data,
            'group_graph_array': group_graph_array,
            'trend': trend
        }

        return jsonify(result)
    
    @staticmethod
    def post(self, args):
        return {
            'success': True,
        }, 201


class SummaryStatistics(Resource):
    @token_required
    def get(self):
        # Get the DataFrame directly
        table_df = get_table_as_dataframe("membrane_proteins")
        pages = Pages(table_df)
        
        check_which_page = request.args.get('stats-data', 'no_where')
        group_field_selection = request.args.get('field_selection', 'species')
        
        parent_data, summary_search_filter_options, group_field_selection = summaryStatisticsConverter(group_field_selection)
        group_dict = find_dict_with_value_in_nested_data(stats_data(), group_field_selection)

        if (check_which_page == "stats-categories"):
            data = parent_data
        else:
            conf = request.args.get('chart_conf', '{"color": "#005EB8", "opacity": 0.9}')
            conf = json.loads(conf)
            group_graph, dataframe = pages.view_dashboard(group_field_selection, conf)
            merged_list = summary_search_filter_options
            sorted_frame = dataframe.sort_values(by='Values', ascending=False).to_dict('records')
            data = {
                "group_dict"    : group_dict,\
                "search_object" : merged_list,
                "data"          : group_graph,
                "headers"       : tableHeader(dataframe.columns),
                "dataframe"     : sorted_frame,
                "search_key"    : group_field_selection,
                "status"        : 'success',
            }
        return jsonify(data)


class SummaryStatisticsLines(Resource):

    def __init__(self):
        pass

    def get(self):
        check_which_page = request.args.get('stats-data', 'no_where')

        group_field_selection = request.args.get('field_selection', 'species')

        parent_data, summary_search_filter_options, group_field_selection = summaryStatisticsConverter(group_field_selection)
        group_dict = find_dict_with_value_in_nested_data(stats_data(), group_field_selection)
        if (check_which_page == "stats-categories"):
            data = parent_data
        else:
            conf = request.args.get('chart_conf', '{"color": "#005EB8", "opacity": 0.9}')
            conf = json.loads(conf)
            group_graph, dataframe = self.pages.view_dashboard(group_field_selection, conf)
            merged_list = summary_search_filter_options
            sorted_frame = dataframe.sort_values(by='Values', ascending=False).to_dict('records')
            data = {
                "group_dict"    : group_dict,\
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
