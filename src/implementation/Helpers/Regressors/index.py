import numpy as np
from sklearn.svm import SVR
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from src.implementation.data.columns.remove_columns import not_needed_columns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.mixture import GaussianMixture
from sklearn.impute import SimpleImputer

class Regressors:

    def __init__(self, data, remove_by_percent):
        self.data = data
        self.remove_empty_by(remove_by_percent)


    
    def run_regressor_algorithm(self, algorithm, **kwargs):
        regressor = algorithm(**kwargs)
        # Create a copy of the dataset to store the imputed values
        imputed_data = self.data.copy()  
        columns = not_needed_columns
        imputed_data = imputed_data.drop(columns, inplace=False, axis=1)
        imputed_data = imputed_data[imputed_data.select_dtypes(include=['float', 'int', 'float64', 'int64']).columns]
        # remove columns with no value
        imputed_data_all_null = imputed_data.columns[imputed_data.isnull().all()].tolist()

        # Select columns not in the exclude list
        selected_columns = imputed_data.columns.difference(imputed_data_all_null)

        imputed_data = imputed_data[selected_columns]
        # fill empty for us to train a model that fills in None /NaN spaces
        imputed_data_ = self.simple_regression(imputed_data, 'mean')

        for target_column in imputed_data_.columns:
            # Split the dataset into two parts: one with complete data for the target column, and one without
            train_data = imputed_data[imputed_data[target_column].notnull()]
            test_data = imputed_data[imputed_data[target_column].isnull()]

            train_data.to_csv("X_train.csv")
            if (not test_data.empty):
                # Separate the features and target column from the training data
                X = train_data.drop(target_column, axis=1)
                y = train_data[target_column]
                # validation for regression
                X_train, X_validation, y_train, y_validation = train_test_split(X, y, test_size=0.2, random_state=42)
                

                # Separate the features from the testing data
                X_test = test_data.drop(target_column, axis=1)
                try:
                    # Train the model
                    regressor.fit(X_train, y_train)

                    # Predict the missing values
                    # y_pred_vali = regressor.predict(X_validation)
                    # mse = mean_squared_error(y_validate, y_pred_vali)
                    
                    # Predict real values after validation
                    # y_pred = regressor.predict(X_test)
                except (Exception, ValueError) as e:
                    print("Column with problem: "+target_column)
                    test_data.to_csv(target_column+".csv")
                    print(str(e))
                    exit()

                # Fill in the missing values in the target column
                # imputed_data.loc[imputed_data[target_column].isnull(), target_column] = y_pred
        return imputed_data_

    # Random Forest
    def random_forest_regressor(self):
        predicted_missing = self.run_regressor_algorithm(RandomForestRegressor)
        return predicted_missing

    # Decision Shift
    def decision_tree_regressor(self):
        predicted_missing = self.run_regressor_algorithm(DecisionTreeRegressor)
        return predicted_missing

    # Agglomerative Clustering
    def gradient_boosting_regressor(self):
        predicted_missing = self.run_regressor_algorithm(GradientBoostingRegressor)
        return predicted_missing

    # OPTICS
    def linear_regression(self):
        predicted_missing = self.linear_regression(LinearRegression)
        return predicted_missing

    def simple_regression(self, dataset, strategy = 'mean'):
        # # Initialize the SimpleImputer with desired strategy (e.g., 'mean', 'median', 'most_frequent')
        imputer = SimpleImputer(strategy=strategy, missing_values=np.NaN, keep_empty_features=True)

        # Fit the imputer on the DataFrame
        imputer.fit(dataset)
        data_formed = imputer.transform(dataset)
        transformed = pd.DataFrame(data_formed)
        # Transform the DataFrame to fill missing values
        df_filled = pd.DataFrame(data_formed, columns=dataset.columns)
        df_filled.to_csv("wjwjjw.csv")
        return df_filled
    
    def remove_empty_by(self, remove_by_percent = 90):
        # Create a copy of the dataset to store the imputed values
        imputed_data = self.data.copy()  
        # Calculate the percentage of None values in each column
        none_percentage = (imputed_data.isna().sum() / len(imputed_data)) * 100

        # Determine columns with over 50% missing values
        needed_columns = none_percentage[none_percentage <= remove_by_percent]

        # get removed columns
        # Get the columns that are not in the excluded_columns list
        removed_columns = [col for col in imputed_data.columns if col not in needed_columns.index]

        # Drop the columns from the DataFrame
        filtered_data = imputed_data[needed_columns.index]

        return filtered_data, needed_columns.index, removed_columns


