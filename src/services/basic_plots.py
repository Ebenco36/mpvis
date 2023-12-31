import pandas as pd
import altair as alt
import random
from src.services.graphs.helpers import Graph
from src.services.Helpers.BasicClasses.GroupByClass import GroupBy
from src.services.exceptions.AxisExceptions import AxisException
from src.services.exceptions.NotFoundOnList import NotFoundOnList
from src.services.exceptions.TagDoesnotExist import TagDoesnotExist
from src.services.Helpers.machine_learning_al.normalization import Normalization
from src.services.data.columns.quantitative.quantitative import cell_columns, rcsb_entries
from src.services.data.columns.quantitative.quantitative_array import quantitative_array_column
from src.services.Helpers.helper import extract_function_names, parser_change_dot_to_underscore, \
    generate_color_palette
from src.services.Helpers.fields_helper import graph_options, graph_types_kit, \
    graph_selection_categories_UI_kit, \
    graph_group_by_date, graph_group_by_others, \
    date_grouping_methods, quantification_fields_kit, \
    multi_select_kit, merge_graph_into_one_kit, normalization_algorithms_helper_kit,\
    graph_combined_types_kit, grouping_aggregation_methods



def home_page_graph(conf):
    group_aggregate_selected_key = 'count'
    statistics_view = GroupBy(df)
    quantitative_data = cell_columns+rcsb_entries+quantitative_array_column
    # replace dot with underscore
    quantitative_replace_dot_with_underscore = parser_change_dot_to_underscore(quantitative_data)
    quantitative_data = tuple(quantitative_replace_dot_with_underscore)
    tab_data = None
    tab_data, pivot_col_ = statistics_view.group_by_years_extra("bibliography_year", list(quantitative_data), group_aggregate_selected_key)
    # st.write(tab_data.head(5))
    graph = Graph(tab_data)
    graph = graph.set_properties([pivot_col_, "cell_angle_alpha"], "")
    altair_graph_home = graph.bar_plot()
    altair_graph_home_ = altair_graph_home\
        .encoding(tooltips = [ 
                pivot_col_,
                "cell_angle_alpha"
            ], 
            encoding_tags = ["ordinal", "quantitative"]
        )\
        .config(conf=conf)\
        .properties(width=500, title="Yearly Releases")\
        .interactive()
        # Display the chart in Streamlit
    return altair_graph_home_.return_dict_obj()


def data_flow(protein_db):
    d = pd.crosstab(protein_db.bibliography_year, columns=protein_db.group).cumsum()

    d = d.stack().reset_index()
    d = d.rename(columns={0:'CummulativeCount'})
    d = d.convert_dtypes()
    # Define a custom color palette
    start_color = '#005EB8'  # Red
    end_color = '#B87200'    # Green

    color_list = ['#93C4F6', '#005EB8', '#D9DE84', '#636B05']

    # Generate a color palette with 10 colors
    num_colors = len(list(protein_db['group'].unique()))
    palette = generate_color_palette(start_color, end_color, num_colors)
    random.shuffle(palette)

    custom_palette = alt.Scale(domain=list(protein_db['group'].unique()),
                           range=color_list[:num_colors])
    entries_over_time = alt.Chart(d).mark_bar(size=15).encode(
        x=alt.X('bibliography_year:O', title="Year"),
        y=alt.Y('CummulativeCount:Q', title = 'Entries'),
        color=alt.Color('group', scale=custom_palette, legend=alt.Legend(title="DB Type", labelLimit=0)),
        tooltip=[alt.Tooltip('CummulativeCount:Q'),
                alt.Tooltip('group'),
                alt.Tooltip('bibliography_year:O')]
    ).configure_legend(orient='bottom').properties(
        width="container",
        height=400,
        title="Database Entries Over Time"
    ).to_dict()
    return entries_over_time

def group_data_by_methods(df, columns=['bibliography_year', 'rcsentinfo_experimental_method'], col_color="rcsentinfo_experimental_method", col_x="bibliography_year"):
    group_subtype_count = df.groupby(columns).size().reset_index(name='Count')
    chart = alt.Chart(group_subtype_count).mark_line().encode(
        x=f'{col_x}:O',
        y='Count:Q',
        color=f'{col_color}:N',
        tooltip=['Count:Q']
    ).configure_legend(orient='bottom').properties(
        width="container",
        title='Counts of Experimental Methods Over the Years'
    ).to_dict()
    return chart

def create_UI_grouped_by():
    group_by = GroupBy(df)
    quantitative_data = cell_columns+rcsb_entries+quantitative_array_column

    # replace dot with underscore
    quantitative_replace_dot_with_underscore = parser_change_dot_to_underscore(quantitative_data)
    quantitative_data = tuple(quantitative_replace_dot_with_underscore)

    # Initialize values here. Could be made better
    group_type = ""
    group_classes = "By Year"
    selection_type = "Date Fields"

    _, selection_type = graph_selection_categories_UI_kit(1)
    if selection_type == "Date Fields":
        _, group_type = graph_group_by_date(1)
    elif selection_type == "Descriptions":
        _, group_type = graph_group_by_others(1)

    _, normalization_algorithm_selection = normalization_algorithms_helper_kit(1)

    # Aggregation methods
    classes_options, group_aggregate_selected = grouping_aggregation_methods(1)


    if selection_type == "Date Fields" and group_type != "":
        _, group_classes = date_grouping_methods(1)
    _, graph_dimension_selection = graph_types_kit(2)

    """
        Single or multiple graphs plotted together.
    """
    _, selected_type = multi_select_kit(1)



    selection_avenue_default, selection_type_default, selection_avenue, _ = graph_options()


    tab_data = None
    pivot_col_ = None
    
    """
        get the key of the selected option for aggregate for the function to compute 
        properly with issues. classes_options is the dictionary that contains all key pair. While 
        group_aggregate_selected is the selected value

    """
    group_aggregate_selected_key = next((key for key, value in classes_options.items() if value == group_aggregate_selected), "sum")

    if selection_type == "Date Fields" and group_classes == "By Year":
        tab_data, pivot_col_ = group_by.group_by_year(group_type, list(quantitative_data), group_aggregate_selected_key)
    elif selection_type == "Date Fields" and group_classes == "By Month":
        tab_data, pivot_col_ = group_by.group_by_month(group_type, list(quantitative_data), group_aggregate_selected_key)
    elif selection_type == "Descriptions":
        tab_data, pivot_col_ = group_by.group_by_other(group_type, list(quantitative_data), group_aggregate_selected_key)
   
    # check if tab_data is empty
    if not tab_data.empty:
        # Save the data point 
        tab_data.to_csv("tab_data_grouped.csv")

        # Once we have a data frame, we can plot aginst other columns from the data frame

        _, quantitative_data_with_kit = quantification_fields_kit(1929, selected_type)

        selected_multiple_graph_view_kit = "no"
        if(len(quantitative_data_with_kit) > 1 and selected_type == "multiple select"):
            _, selected_multiple_graph_view_kit = merge_graph_into_one_kit(1)

        if selected_multiple_graph_view_kit == 'yes':
            _, graph_format_selection = graph_combined_types_kit(1)
        
        # Normalization
        df_ = tab_data[quantitative_replace_dot_with_underscore]
        normalize = Normalization(df_)
        normalized_df = getattr(normalize, str(normalization_algorithm_selection).replace(' ', '_'))()

        processed_df = pd.concat([tab_data[pivot_col_].reset_index(drop=True), normalized_df.reset_index(drop=True)], axis=1)

        # display table view for grouped data.
        # st.write(processed_df)
        
        try:
            graph = Graph(processed_df)

            if selected_type == "single select":
                graph = graph.set_properties([pivot_col_, quantitative_data_with_kit], "", selection_avenue_default, selection_type_default)
                altair_graph_obj = getattr(graph, str(graph_dimension_selection).replace(' ', '_'))()
                altair_graph_objj = altair_graph_obj\
                    .encoding(
                        tooltips = [ 
                            pivot_col_,
                            quantitative_data_with_kit
                        ], 
                        encoding_tags = ["ordinal", "quantitative"]
                    )\
                    .get_selection_avenue(selection_avenue)\
                    .config()\
                    .properties(width=1000)\
                    .interactive()
                # Display the chart in Streamlit
                altair_graph_objj.return_dict_obj()
            else:
                # for merging graph into 1
                graph_lists = []
                # loop through for each graph
                num_columns = 3

                for vis_index in range(0, len(quantitative_data_with_kit)):

                    # Calculate the column and row indices
                    column = vis_index % num_columns

                    graph = graph.set_properties([pivot_col_, quantitative_data_with_kit[vis_index]], "", selection_avenue_default, selection_type_default)
                    altair_graph_obj = getattr(graph, str(graph_dimension_selection).replace(' ', '_'))()
                    altair_graph_objj = altair_graph_obj\
                        .encoding(tooltips = [], encoding_tags = ["ordinal", "quantitative"])
                    
                    if(selected_multiple_graph_view_kit == "no"):
                        # Display the chart in Streamlit
                        altair_graph_objj.get_selection_avenue(selection_avenue)\
                            .config()\
                            .properties(width=300)\
                            .interactive()\
                            .return_dict_obj()                                           
                    else:
                        graph_lists.append(altair_graph_objj.return_obj())
                if(selected_multiple_graph_view_kit == "yes"):
                    # This isn't working yet! In progress
                    altair_multi_graph_obj = getattr(graph, str(graph_format_selection).replace(' ', '_'))(graph_lists)
                    altair_multi_graph_obj

        except (AxisException, NotFoundOnList, TagDoesnotExist) as ex:
            print(str(ex))

    else:
        print("We can not seems for get data frame for this visual.")