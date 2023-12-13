import sys
import pandas as pd
from utils.general import shorten_column_name
from src.implementation.Helpers.EDA.EDA import EDA
from src.implementation.graphs.helpers import Graph
from src.implementation.visualization import DataImport
from src.implementation.Helpers.BasicClasses.GroupByClass import GroupBy
from src.implementation.data.columns.remove_columns import not_needed_columns
from src.implementation.Helpers.helper import NAPercent, parser_change_dot_to_underscore, \
    generate_range_bins, generate_list_with_difference, convert_to_numeric_or_str, convert_to_type
from src.implementation.range_order import columns_range_limit
from src.Dashboard.data import array_string_type

class Pages:

    def __init__(self, data):
        self.data = data
        self.grouping = GroupBy(self.data)
        self.selected_columns_to_vis = []
        self.chunked_data = None
        

    def dashboard_helper(self, group_by_column = ''):
        # replace dot with underscore
        quantitative_replace_dot_with_underscore = parser_change_dot_to_underscore(self.data.columns)
        quantitative_data = tuple(quantitative_replace_dot_with_underscore)
        # Group the data by the 'Category' column
        grouped_data = self.data.groupby(group_by_column).size()
        grouped_data = grouped_data.reset_index()
        grouped_data = pd.DataFrame(grouped_data)
        grouped_data.columns = [group_by_column, "Values"]

        return grouped_data, group_by_column
    
    def dashboard_helper_exemption(self, group_by_column = 'resolution', range_name="range_value", range_resolution_meters=0.2):
        
        group_by_column = shorten_column_name(group_by_column)
        
        if ( not '*' in group_by_column and group_by_column != ""):
            # Apply the custom function to 'Column1'
            self.data[group_by_column] = self.data[group_by_column].apply(convert_to_numeric_or_str)

            # Convert string list to list
            self.data['rcsentinfo_software_programs_combined'] = self.data['rcsentinfo_software_programs_combined'].apply(lambda x: convert_to_type(x))
            
            # Separate string column
            mask_str = self.data[group_by_column].apply(lambda x: isinstance(x, str))
            df_numeric = self.data[~mask_str]
            df_str = self.data[mask_str]
            max_value = df_numeric[group_by_column].max(skipna=True)
            if(not df_numeric.empty and not pd.isna(max_value) and group_by_column != "rcsentinfo_software_programs_combined"):
                # Convert 'selected column' column to numeric values in the numeric DataFrame
                df_numeric[group_by_column] = pd.to_numeric(df_numeric[group_by_column], errors='coerce')

                max_range_meters = round(max_value)
                range_bins = generate_range_bins(range_resolution_meters, max_range_meters)
                generated_list = generate_list_with_difference(len(range_bins), range_resolution_meters)

                # Define custom bins for range grouping in the numeric DataFrame
                bins = generated_list
                labels = range_bins

                # Create a new column 'range_name' based on the range of 'Species' values in the numeric DataFrame
                df_numeric[range_name] = pd.cut(df_numeric[group_by_column], bins=bins, labels=labels[:-1], right=False)

                # Group by 'group_by_column' in the numeric DataFrame and sum the 'Value' for each range
                grouped_numeric_data = df_numeric.groupby(range_name).size().reset_index()

                grouped_str_data = df_str.groupby(group_by_column).size().reset_index()
                
                # Concatenate the dataframes vertically
                merged_df = pd.concat([grouped_numeric_data, grouped_str_data], ignore_index=True)

                # Convert 'Column1' to object data type
                merged_df[range_name] = merged_df[range_name].astype('object')
                merged_df[group_by_column] = merged_df[group_by_column].astype('object')

                # Update 'Column1' with 'Column2' values where 'Column1' is NaN
                merged_df[range_name].fillna(merged_df[group_by_column], inplace=True)

                # Drop the 'extra if exist' column
                merged_df.drop(group_by_column, axis=1, inplace=True)
                merged_df.columns = [group_by_column, "Values"]
            elif (group_by_column in array_string_type()):
                # Method 2: Using value_counts
                all_names = [name for names_list in self.data[group_by_column] for name in names_list]
                merged_df = pd.Series(all_names).value_counts().reset_index()
                merged_df.columns = [group_by_column, 'Values']
            else:
                # replace dot with underscore
                quantitative_replace_dot_with_underscore = parser_change_dot_to_underscore(self.data.columns)
                quantitative_data = tuple(quantitative_replace_dot_with_underscore)
                # Group the data by the 'Category' column
                grouped_data = self.data.groupby(group_by_column).size()
                grouped_data = grouped_data.reset_index()
                grouped_data = pd.DataFrame(grouped_data)
                grouped_data.columns = [group_by_column, "Values"]
                merged_df = grouped_data
        else:
            # group by column here follows this format parent_tag*search_key
            search_key = group_by_column.split('*')
            
            merged_df_ = self.data[self.data[search_key[0]] == search_key[1]]
            # Group by year and 'Category', and count records
            merged_df = merged_df_.groupby([
                merged_df_['bibliography_year'], 
                search_key[0]
            ]).size().reset_index(name='Values')
            group_by_column = "bibliography_year"

            # merged_df = merged_df[['bibliography_year', 'Values']]

        # Filter rows where 'Age' column value is greater than zero
        merged_df = merged_df[merged_df["Values"] > 0]

        # # Sort the DataFrame in ascending order based on 'Age'
        merged_df = merged_df.sort_values(by='Values')

        # Rearrange the index based on the sorted order
        merged_df = merged_df.reset_index(drop=True)

        return merged_df, group_by_column
        

    def view_dashboard(self, get_query_params, conf={}):
        # Get the URL parameters using Streamlit routing
        selected_content = get_query_params

        range_resolution_meters = columns_range_limit.get(selected_content) if columns_range_limit.get(selected_content) else 0.2
        df_, pivot_col_ = self.dashboard_helper_exemption(selected_content, "range_values", range_resolution_meters)
        
        # Resetting the index to maintain the original order
        df_.reset_index(drop=True, inplace=True)

        # sort records and get the first 20
        sorted_df = df_.sort_values(by='Values', ascending=False).head(20)
    
        chart_obj = Graph.plot_bar_chart(sorted_df, pivot_col_, conf).to_dict()
        return chart_obj, df_

    def EDA_view(self, selected_chunk_perc=10, selected_columns_to_vis:list=[]):
        perc = [i for i in range(10, 101, 10)]
        # Create a sidebar with page selection dropdown
        data = self.remove_emptiness_with_percentage(selected_chunk_perc)
        self.chunked_data = data
        # Create a sidebar with page selection dropdown
        selected_columns_to_vis = st.sidebar.multiselect("Select Columns", data.columns.tolist())
        if(selected_columns_to_vis):
            # set globally
            self.selected_columns_to_vis = selected_columns_to_vis
            self.chunked_data = data[selected_columns_to_vis]

        return self.EDA_data_summary(), self.EDA_correlation_matrix_plot(), self.EDA_outlier_plot()



    def EDA_base(self, data):
        data_ = data.iloc[:, 0:]

        eda = EDA(data_)

        return eda

    def EDA_data_summary(self):
        eda = self.EDA_base(self.chunked_data)
        summary = eda.summary_statistics()
        return summary
    
    def EDA_outlier_plot(self):
        eda = self.EDA_base(self.chunked_data)
        outlier = Graph.outlier_visualization(eda.get_data())

        return outlier

    def EDA_correlation_matrix_plot(self):
        eda = self.EDA_base(self.chunked_data)
        correlation_matrix = eda.correlation_matrix()
        # Step 3: Reshape the correlation matrix for plotting
        correlation_matrix = correlation_matrix.stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})

        correlation_matrix['correlation_label'] = correlation_matrix['correlation']
        graph = Graph.correlation_matrix(correlation_matrix, ['variable2:O', 'variable:O'], "correlation:Q" , "correlation_label")

        return graph
    
    def remove_emptiness_with_percentage(self, perc = 50):
        df = self.data.drop(not_needed_columns, inplace=False, axis=1)
        df = df[df.select_dtypes(include=['float', 'int', 'float64', 'int64']).columns]
        # get percentage of emptiness
        NA = NAPercent(df)
        NA['NA Percent']
        NA['NA Percent'] = NA['NA Percent'].astype(float)

        NA.to_csv("NAPercent.csv")

        df_columns = NA[NA['NA Percent'] < perc].index.tolist()

        # We can use this for further analysis
        df_great = df[df_columns]

        NA.to_csv("NAChunkedDF.csv")

        return df_great