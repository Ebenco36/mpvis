import os
import pandas as pd
from pathlib import Path
import json
from src.implementation.visualization import DataImport
from flask import jsonify, request
from sklearn.model_selection import train_test_split
from src.implementation.Helpers.helper import removeUnderscoreIDFromList
from src.implementation.Helpers.Regressors.index import Regressors
from src.implementation.Helpers.machine_learning_al.dimensionality_reduction import DimensionalityReduction
from src.implementation.data.columns.remove_columns import not_needed_columns
from src.implementation.Helpers.machine_learning_al.normalization import Normalization
from src.implementation.Helpers.machine_learning_al.sklearnML import MachineLearning
from src.implementation.Helpers.helper import create_json_response
from src.implementation.Helpers.helper import tableHeader
from flask_restful import Resource, reqparse

class UOT(Resource):
    def __init__(self):

        data_import = DataImport()

        self.dataset = data_import.loadFile()

        self.dataset.drop(columns=not_needed_columns, inplace=True)

        self.parser = reqparse.RequestParser()

    

    def get(self):
        # Get the pagination parameters from the query string
        page = request.args.get('request-type', 'stage1')
        # Session name to create a folder for current user
        session_name = request.args.get('session_name', 'Ebenezer_Awotoro_001')
        
        path = "./public/data_sessions/" + session_name

        if(page == "stage1"):
            return self.get_attributes()
        elif(page == "stage2"):
            method = request.args.get('method', 'simple_regressor')
            allowed_perc_of_emptiness = request.args.get('allowed_perc_of_emptiness', 10)
            return self.manage_missing_values(path, method, allowed_perc_of_emptiness) 


    def post(self):
        # Get the pagination parameters from the query string
        page = request.args.get('request-type', 'stage2')
        # Target column as label
        training_or_testing = request.args.get('training_or_testing', "training")
        # Get JSON data from the POST request
        post_data = request.get_json()
        
        # Target column as label
        target = post_data.get('target', 'Resolution')
        session_name = post_data.get('session_name', 'Ebenezer_Awotoro_001')
        path = "./public/data_sessions/" + session_name

        if(page == "stage2"):
            selected_column = post_data.get('selected_column', [])
            return self.get_data_for_selected_attributes(target, selected_column, session_name)
        elif(page == "stage3"):
            # Target column as label
            split_ratio = post_data.get('split_ratio', 0.2)
            return self.generate_train_test_split(path=path, target=target, split_ratio=split_ratio)
        elif(page == "stage4"):
            # Target column as label
            method = post_data.get('method', "min_max_normalization")
            return self.normalization_stage(path, method, training_or_testing)
        elif(page == "stage5"):
            # Target column as label
            method = post_data.get('method', "pca_algorithm")
            pca_features = post_data.get('pca_features', 2)
            return self.dimensionality_reduction(path, method, training_or_testing, pca_features)
        
    def get_attributes(self):
        # Remove columns without any content
        df_cleaned = self.dataset.dropna(axis=1, how='all')
        myList =  df_cleaned.select_dtypes(include=['number', 'int', 'float']).columns.tolist()
        header = sorted(removeUnderscoreIDFromList(myList))

        return create_json_response(
            httpResponse=True, 
            data=header, 
            status=True, 
            status_code=200, 
            message="Headers fetch successfully"
        )



    def get_data_for_selected_attributes(self, target_column:str, selected_column:list, session_name:str):
        # Append the target column for test
        selected_column.append(target_column)
        """
            Generate a portion of dataset for the case
            Select the first 500 data for users to play around with
        """
        data = self.dataset[selected_column].iloc[: 500]
        """
            Store a session folder that contains content of selected dataset
            create directory if does not exist
        """
        # Check if the directory exists
        directory_path = "./public/data_sessions/" + session_name
        if not os.path.exists(directory_path):
            # Create the directory
            os.makedirs(directory_path)
            
        path = "./public/data_sessions/" + session_name + "/dataset.csv"
        data.to_csv(path)
        # remove NaN and replace with empty string
        nonNaN = data.fillna('')
        response = {
            "data": nonNaN.to_dict('records'),
            "header": tableHeader(data.columns),
            "path": path,
        }

        return create_json_response(
            httpResponse=True, 
            data=response, 
            status=True, 
            status_code=200, 
            message="Retrieve content successfully"
        )



    def generate_train_test_split(self, split_ratio:float, path:str, target:str):
        df = pd.read_csv(path + "/dataset_missing.csv", low_memory=False)
        df.drop(columns=['Unnamed: 0'], inplace=True)
        """
            Generate data split for training and testing
        """
        # Split the data into train and test sets
        train_data, test_data, train_target, test_target = train_test_split(
            df.loc[:, df.columns != target],  # Features selected by users
            df[target],  # Target
            test_size=float(split_ratio),  # Percentage of data for testing (0.2 = 20%)
            random_state=42  # Seed for randomization, for reproducibility
        )

        # save datasets splits
        train_data.to_csv(path + "/dataset_train.csv")
        test_data.to_csv(path + "/dataset_test.csv")
        train_target.to_csv(path + "/dataset_train_target.csv")
        test_target.to_csv(path + "/dataset_test_target.csv")

        # Return response
        response = {
            "train_data": train_data.to_dict('records'), 
            "test_data": test_data.to_dict('records'), 
            "train_headers": tableHeader(train_data.columns), 
            "test_headers": tableHeader(test_data.columns),
            # "train_target": train_target.to_dict('records'), 
            # "test_target": test_target.to_dict('records')
        }

        return create_json_response(
            httpResponse=True, 
            data=response, 
            status=True, 
            status_code=200, 
            message="Retrieve training and split data successfully"
        )



    def manage_missing_values(self, path:str, method:str, allowed_perc_of_emptiness=10):
        """
            Provide options for filling in missing values
        """
        df = pd.read_csv(path + "/dataset.csv", low_memory=False)
        df.drop(columns=['Unnamed: 0'], inplace=True)
        target = df.iloc[:, -1]
        df = df.loc[:, df.columns != target.name]
        # Select method to fill emptiness
        Missing_algorithm = Regressors(df, allowed_perc_of_emptiness)
        data = getattr(Missing_algorithm, str(method))()
        response = data.get("data")

        if(data and data.get("status")):
            dataframe = pd.concat([data.get('data'), target], axis=1)
            # Save the dataframe for the next phase
            dataframe.to_csv(path + "/dataset_missing.csv")
            data['data'] = dataframe.to_dict('records')

            response = {
                "header": tableHeader(dataframe.columns),
                "data": data.get('data'),
            }
        """
            This is needed on the split stage
        """
    
        return create_json_response(
            httpResponse=True,
            data = response, 
            message=data.get("message"), 
            error_message=data.get("error_message"), 
            status=data.get("status")
        )
    

    def normalization_stage(self, path:str, method:str, training_or_testing="training"):
        """
            Normalize data for optimal result
        """

        if (training_or_testing == "training"):
            df = pd.read_csv(path + "/dataset_train.csv", low_memory=False)
        else:
            df = pd.read_csv(path + "/dataset_test.csv", low_memory=False)
        df.drop(columns=['Unnamed: 0'], inplace=True)
        # Select method to fill emptiness

        Normalization_algorithm = Normalization(df)
        data = getattr(Normalization_algorithm, str(method))()

        # Save the dataframe for the next phase
        data.to_csv(path + "/dataset_" + training_or_testing + "_normalized.csv")
        """
            This is needed on the split stage
        """
        response = {
            "data": data.to_dict('records'),
            "headers": tableHeader(data.columns)
        }
        return create_json_response(
            httpResponse=True, 
            data=response, 
            status=True, 
            status_code=200, 
            message="Retrieved normalized successfully"
        )


    def dimensionality_reduction(self, path:str, method:str, training_or_testing="training", pca_features=2):
        """
            We can proceed with this if atrributes selected are more the 2
        """
        df = pd.read_csv(path + "/dataset_" + training_or_testing + "_normalized.csv", low_memory=False)
        df.drop(columns=['Unnamed: 0'], inplace=True)

        # Select method to fill emptiness
        pca_columns=["PCA_"+str(i) for i in range(1, int(pca_features)+1)]

        DR_algorithm = DimensionalityReduction(X=df, n_features=int(pca_features), pca_columns=pca_columns)
        data, explainability = getattr(DR_algorithm, str(method))()

        # Save the dataframe for the next phase
        data.to_csv(path + "/dataset_" + training_or_testing + "_dimensionalized.csv")
        """
            This is needed on the split stage
        """
        # print(explainability)
        response = {
            "data": data.to_dict('records'),
            "headers": tableHeader(data.columns),
            "explainability": explainability,
        }
        return create_json_response(
            httpResponse=True, 
            data=response, 
            status=True, 
            status_code=200, 
            message="Retrieved dimensionalized data successfully"
        )


    def implement_clustering(self, path:str, method:str):
        """
            Allow various clustering algorithm options for user to understand the base concept
        """
        df = pd.read_csv(path, low_memory=False)
        df.drop(columns=['Unnamed: 0'], inplace=True)
        # Select method to fill emptiness

        # ML_algorithm = MachineLearning(X=df, eps=eps, min_samples=min_samples, n_clusters=n_clusters, n_components=n_components)
        # classified_, params  = getattr(ML_algorithm, str(method))()

        # print(data)


    def ML_explainability_implementation():
        """
            Explain reason for the immediate above methods
        """
        pass


    def data_summary():
        """
            Generate data summary of selected attributes
        """
        pass



    
