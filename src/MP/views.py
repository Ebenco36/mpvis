import json
from flask import request, send_file
from flask_restful import Resource, reqparse
from src.Dashboard.services import export_to_csv, export_to_excel
from src.MP.services import DataService
from src.utils.response import ApiResponse


class DataResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('experimental_method', type=str, help='select resolution method')
        self.parser.add_argument('download', type=str, help='download data as well')
        
    def get(self):
        # Access query parameters from the URL
        experimental_method = request.args.get('experimental_method', None)
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
            data = DataService.get_data_by_column_search("rcsentinfo_experimental_method", experimental_method)
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