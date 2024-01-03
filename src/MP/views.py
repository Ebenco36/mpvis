import json
import altair as alt
from flask import request, send_file
from flask_restful import Resource, reqparse
from src.Dashboard.services import export_to_csv, export_to_excel
from src.MP.machine_learning_services import UnsupervisedPipeline
from src.services.Helpers.fields_helper import dimensionality_reduction_algorithms_helper_kit, machine_algorithms_helper_kit, missing_algorithms_helper_kit, normalization_algorithms_helper_kit, transform_data_view
from src.services.graphs.helpers import Graph
from src.MP.services import DataService
from src.MP.data import cat_list
from src.utils.response import ApiResponse


class DataResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('experimental_method', type=str, help='select resolution method')
        self.parser.add_argument('download', type=str, help='download data as well')
        
    def get(self):
        # Access query parameters from the URL
        experimental_method = request.args.get('experimental_method', None)
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        
        # download format
        download = request.args.get('download', None)
        if(download):
            data = DataService.get_data_by_column_search_download("rcsentinfo_experimental_method", experimental_method)
            if(download == "csv"):
                filename = 'output_data.csv'
                export_to_csv(data['data'], filename)
                return send_file(filename, as_attachment=True)
            elif(download == "xlsx"):
                filename = 'output_data.xlsx'
                export_to_excel(data['data'], filename)
                return send_file(filename, as_attachment=True)
        else:
            # page default
            data = DataService.get_data_by_column_search("rcsentinfo_experimental_method", experimental_method, page, per_page)
            if(data):
                return ApiResponse.success(data, "Fetch records successfully.")
            else: 
                return ApiResponse.error("Not found!", 404)
        

class CategoricalDataResource(Resource):
    def get(self):
        data = DataService.get_unique_values_for_categorical_columns()
        if(data):
            return data
        else: 
            return ApiResponse.error("Not found!", 404)
        


class DataFilterResource(Resource):
    def __init__(self):
        pass
        
    def get(self):
        dimensionality_list = dimensionality_reduction_algorithms_helper_kit()
        normalization_list = normalization_algorithms_helper_kit()
        machine_list = machine_algorithms_helper_kit()
        regressors_list = missing_algorithms_helper_kit()
        categorical_column_list = transform_data_view(cat_list, 'categorical_columns', 'single', [], False)
        methods = ["All", "EM", "Multiple methods", "NMR", "X-ray"]
        experimental_method = transform_data_view(methods, 'methods_list', 'single', [], False)
        excluded_fields = ["reflns", "refine", "rcsb_", "diffrn", "exptl", "cell_", "group_", "subgroup_", "species_"]
        excluded_list = transform_data_view(excluded_fields, 'methods_list', 'multiple', [], False)
        filter_list = {
            "experimental_method_list": experimental_method,
            "categorical_list": categorical_column_list,
            "dimensionality_list": dimensionality_list,
            "normalization_list": normalization_list,
            "regressors_list": regressors_list,
            "excluded_list": excluded_list,
            "machine_list": machine_list
        }
        return ApiResponse.success(filter_list, "Fetch filter list successfully.")
            
         
class UsupervisedResource(Resource):
    def post(self):
        data = request.get_json()
        if data and data != "":
            machine_list = data.get('machine_list', "kMeans_clustering")
            regressors_list = data.get('regressors_list', "KNN_imputer_regressor")
            normalization_list = data.get('normalization_list', "min_max_normalization")
            dimensionality_list = data.get('dimensionality_list', "pca_algorithm")
            experimental_method = data.get('experimental_method_list', "X-ray")
            excluded_fields = data.get('excluded_list', [])
            color_by = data.get('categorical_list', "species")
        else:
            machine_list = "kMeans_clustering"
            regressors_list = "KNN_imputer_regressor"
            normalization_list = "min_max_normalization"
            dimensionality_list = "pca_algorithm"
            experimental_method = "X-ray"
            excluded_fields = []
            color_by = "species"
        
        experimental_method = None if experimental_method == "All" else experimental_method
        
        
        """
            We are adding this to the filter. Either to use categorical data or not.
            
        """
        # dimensionality reduction columns
        get_column_tag = dimensionality_list.upper().split("_")[0]
        dr_columns = [ get_column_tag + str(char) for char in range(1, 3)]
        
        # Replace 'your_data_frame' with the actual variable holding your DataFrame
        data_frame = DataService.get_data_by_column_search_download("rcsentinfo_experimental_method", experimental_method)['data']
        result = (
            UnsupervisedPipeline(data_frame)
                .dataPrePreprocessing()
                .modify_dataframe(excluded_fields)
                .select_numeric_columns()
                .apply_imputation(imputation_method=regressors_list, remove_by_percent=90)
                .apply_normalization(normalization_method=normalization_list)
                .apply_dimensionality_reduction(reduction_method=dimensionality_list, n_features=2, dr_columns=dr_columns)
                .apply_clustering(method=machine_list, n_clusters=3)
                .prepare_plot_DR(group_by=color_by)
        )
        
        # ML Plot 
        label="classes"
        result[label] = result['clustering'].apply(lambda x:  str(x) + "_Cluster")
        scatter_plot = Graph(result, axis = dr_columns, labels=label)\
            .scatter_plot()\
            .set_selection(type='single', groups=[label, color_by])\
            .encoding(
                tooltips = result.columns, 
                encoding_tags = ["quantitative", "quantitative"]
            )\
            .properties(width=0)\
            .legend_config()\
            .add_selection()\
            .interactive()
    
        # Convert the Altair chart to a dictionary
        chart_dict = scatter_plot.return_dict_obj()
        
        
        scatter_plot_DR = Graph(result, axis = dr_columns, labels=color_by)\
            .scatter_plot()\
            .set_selection(type='single', groups=[color_by])\
            .encoding(
                tooltips = result.columns, 
                encoding_tags = ["quantitative", "quantitative"]
            )\
            .properties(width=0)\
            .legend_config()\
            .add_selection()\
            .interactive()
            
        # Convert the Altair chart to a dictionary
        chart_dict_DR = scatter_plot_DR.return_dict_obj()

        resp = {
            'data': result.to_dict(orient='records'), 
            'chart': chart_dict,
            'DR_chart': chart_dict_DR,
        }
        return ApiResponse.success(resp, "Fetch records successfully.")