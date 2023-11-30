from flask_restful import Resource
from flask import send_file
from werkzeug.security import safe_str_cmp
from src.implementation.pages import Pages
from src.User.model import UserModel
from src.models.schemas.user import UserSchema, user_summary
import json
from flask import jsonify, request
from src.implementation.Helpers.helper import tableHeader
from src.middlewares.auth_middleware import token_required
from src.implementation.data.training_dataset.dataset import data
user_schema = UserSchema()


class Tutorial(Resource):
    def __init__(self):
        self.tutorial_dataset = data

    # @staticmethod
    # @token_required
    def get(self):
        action = str(request.args.get('action', 'view'))
        
        if(action == 'view'):
            resp = self.tutorial_dataset
            message = "Retrieve tutorial dataset successfully"

        elif (action == 'download'):
            file_name = str(request.args.get('file_name', 'seeds_dataset.csv'))
            # get file name to download
            # Define the path to your CSV file
            csv_file_path = 'fruit_dataset_encoded_clustered.csv'
            
            # Provide a filename for the downloaded file
            filename = 'fruit_data.csv'

            # Use send_file to send the CSV file as a downloadable attachment
            resp = send_file(
                csv_file_path, 
                as_attachment=True, 
                attachment_filename =filename
            )
            message = "Successfully generated dataset"
        else:
            resp = "We don't know what you are talking about."
        
        result = {
            "data": resp,
            "message": message
        }
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


class SummaryStatisticsLines(Resource):

    def __init__(self):
        pass

    def get(self):
        check_which_page = request.args.get('stats-data', 'no_where')

        group_field_selection = request.args.get('field_selection', 'Species')

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