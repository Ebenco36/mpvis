from src.implementation.Helpers.helper import extract_function_names, replace_and_separate, \
    filter_list, format_string_caps
from src.implementation.data.columns.dates import dates_columns
from src.implementation.data.columns.norminal import descriptors, all_descriptors
from src.implementation.data.columns.quantitative.quantitative import cell_columns, rcsb_entries
from src.implementation.data.columns.quantitative.quantitative_array import quantitative_array_column

def graph_options(kit_id:int = 0):
    # default selections for graphs
    selection_avenue_default = ["click", "drag"]
    selection_type_default = ["multiple", "single", "interval"]

    selection_avenue_default = transform_data_view(selection_avenue_default, 'selection_avenue_default', 'single')
    selection_type_default = transform_data_view(selection_type_default, 'selection_type_default', 'single')

    return selection_avenue_default, selection_type_default


def graph_types_kit(kit_id:int=0):
    # Graph Dimension
    file_path_graph = 'src\implementation\graphs\helpers.py'
    graph_dimensions = filter_list(extract_function_names(file_path_graph), "_plot")

    graph_types = transform_data_view(graph_dimensions, 'graph_types', 'single')
    return graph_types

def graph_combined_types_kit(kit_id:int=0):
    # Graph Dimension
    file_path_graph = 'src\implementation\graphs\helpers.py'
    graph_dimensions = filter_list(extract_function_names(file_path_graph), "_plot")

    graph_types = transform_data_view(graph_dimensions, 'graph_types', 'single')

    return graph_types


def machine_algorithms_helper_kit(kit_id:int=0):
    # ML algorithms
    file_path_ml = 'src\implementation\Helpers\machine_learning_al\sklearnML.py'
    ml_algorithms = filter_list(extract_function_names(file_path_ml), "_clustering")

    ML_types = transform_data_view(ml_algorithms, 'ML_types', 'single')

    return ML_types


def missing_algorithms_helper_kit(kit_id:int=0):
    # ML algorithms
    file_path_missing = 'src\implementation\Helpers\Regressors\index.py'
    missing_algorithms = filter_list(extract_function_names(file_path_missing), "_regressor")

    Missing_types = transform_data_view(missing_algorithms, 'Missing_types', 'single')

    return Missing_types


def perc_of_missing_value_kit(kit_id:int = 0):
    # allowed percentage of missing values
    perc = [str(i) for i in range(10, 100, 10)]

    perc_missing_value = transform_data_view(perc, 'perc_missing_value', 'single')

    return perc_missing_value


def dimensionality_reduction_algorithms_helper_kit(kit_id:int=0):
    # DR algorithms
    file_path_dr = 'src\implementation\Helpers\machine_learning_al\dimensionality_reduction.py'
    dr_algorithms = filter_list(extract_function_names(file_path_dr), "_algorithm")
    
    DR_types = transform_data_view(dr_algorithms, 'DR_types', 'single')

    return DR_types


def normalization_algorithms_helper_kit(kit_id:int=0):
    # Normalization algorithms
    file_path_normal = 'src\implementation\Helpers\machine_learning_al\/normalization.py'
    normal_algorithms = filter_list(extract_function_names(file_path_normal), "_normalization")

    normal_types = transform_data_view(normal_algorithms, 'normal_types', 'single')

    return normal_types



def graph_selection_categories_UI_kit(kit_id:int=0):
    options=["Date Fields", "Descriptions"]

    graph_selection_categories = transform_data_view(options, 'graph_selection_categories', 'single')

    return graph_selection_categories



def graph_group_by_date(kit_id:int = 0):
    dates_data = dates_columns
    # replace dot with underscore
    dates_data = tuple([str(s).replace('.', '_') for s in dates_data])

    dates_types = transform_data_view(dates_data, 'dates_types', 'single')

    return dates_types


def graph_group_by_others(kit_id:int = 0):
    desc = all_descriptors
    # replace dot with underscore
    desc = tuple([str(s).replace('.', '_') for s in desc])

    graph_group_by = transform_data_view(desc, 'graph_group_by', 'single')

    return graph_group_by


def date_grouping_methods(kit_id:int = 0):
    classes_options=["By Year", "By Month"]

    date_group_by = transform_data_view(classes_options, 'date_group_by', 'single')
    return date_group_by

def grouping_aggregation_methods(kit_id:int = 0):
    classes_options={ 
        "mean": "Mean", 
        "median": "Median", 
        "sum": "Sum", 
        "min": "Minimum", 
        "max": "Maximum ", 
        "count": "Count",
        "std": "Standard Deviation",
        "var": "Variance"
    }
    
    aggregate_options = {
        "options": [{"value": key, "name": format_string_caps(classes_options[key])} for key in classes_options],
        "model_name": [],
        "safe_name" : "name",
        "field_name": format_string_caps("aggregate_options"),
        "multiple": False,
    }
    return aggregate_options


def multi_select_kit(kit_id:int=0):
    select_options = ["single select", "multiple select"]
    select_options_ = transform_data_view(select_options, 'select_options', 'single')

    return select_options_

def quantification_fields_kit(kit_id:int=0, selection_type:str = "single select"):
    # Quantifications
    quantitative_data = cell_columns+rcsb_entries+quantitative_array_column

    quantitative_attributes = transform_data_view(quantitative_data, 'quantitative_attributes', 'multiple')

    return quantitative_attributes

def merge_graph_into_one_kit(kit_id:int=0):
    merge_graph_options = ["no", "yes"]
    merge_graph_options = transform_data_view(merge_graph_options, 'merge_graph_option', 'single')
    return merge_graph_options


def ml_slider_selector(quantitative_data):
    """
        Select these option based on the ML selected
    """
    option_list = len(quantitative_data) if len(quantitative_data) >=2 else 2
    eps_slider = [0.1, 10.0, 0.3]
    pca_features_slider = option_list
    min_samples_slider = option_list
    n_clusters_slider = option_list
    n_components_slider = option_list

    # date_group_by = transform_data_view(classes_options, 'date_group_by')

    return eps_slider, pca_features_slider, min_samples_slider, n_clusters_slider, n_components_slider



def dataSplitPercOption():
    start = 0.1
    end = 0.5
    step = 0.1  # Adjust the step size based on your preference
    numbers = [str(round(start + i * step, 1)) for i in range(int((end - start) / step) + 1)]
    data = transform_data_view(numbers, 'data_split_perc_option', 'single')

    return data

def PCAComponentsOption(n_features = 2):
    data = [str(i) for i in range(2, int(n_features)+1)]
    data = transform_data_view(data, 'PCA_n_feature_option', 'single')

    return data


def transform_data_view(data, unique_field_name, multiple_selection):
    data_object = {
        "options": [{"value": value, "name": format_string_caps(replace_and_separate(value))} for value in data],
        "model_name": [],
        "safe_name" : "name",
        "field_name": format_string_caps(unique_field_name),
        "multiple": True if multiple_selection == "multiple" else False,
        "tooltip": "",
    }

    return data_object