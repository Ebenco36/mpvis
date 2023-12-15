from src.Dashboard.data import stats_data
from utils.general import shorten_column_name
from src.Dashboard.services import get_table_as_dataframe, get_table_as_dataframe_download, get_table_as_dataframe_exception

class DataService:
    @staticmethod
    def get_data_by_column_search(column_name="rcsentinfo_experimental_method", value="X-ray", page=1, per_page=10):
        data = get_table_as_dataframe_exception("membrane_proteins", column_name, value, page, per_page)
        return data
    
    @staticmethod
    def get_data_by_column_search_download(column_name="rcsentinfo_experimental_method", value="X-ray"):
        data = get_table_as_dataframe_download("membrane_proteins", column_name, value)
        return data
    
    # Define a function to retrieve unique values for categorical columns
    def get_unique_values_for_categorical_columns():
        table_columns = stats_data()
        # Collect unique values using a set
        unique_values = set()
        for entry in table_columns:
            for item in entry['data']:
                unique_values.add(shorten_column_name(item['value'].split('*')[0]))

        # Convert the set to a list if needed
        unique_columns = list(unique_values)
        unique_values = {}

        df = get_table_as_dataframe("membrane_proteins")
        # Retrieve unique values for each categorical column
        for column_name in unique_columns:
            print(df[column_name].unique())
            unique_values[column_name] = df[column_name].unique()

        return unique_values