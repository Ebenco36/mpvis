from src.implementation.Helpers.helper import extract_function_names
from src.implementation.data.columns.dates import dates_columns
from src.implementation.data.columns.norminal import descriptors, all_descriptors
from src.implementation.data.columns.quantitative.quantitative import cell_columns, rcsb_entries
from src.implementation.data.columns.quantitative.quantitative_array import quantitative_array_column

def graph_options(kit_id:int = 0):
    # default selections for graphs
    selection_avenue_default = ["click", "drag"]
    selection_type_default = ["multiple", "single", "interval"]
    return selection_avenue_default, selection_type_default



def graph_types_kit(kit_id:int=0):
    # Graph Dimension
    file_path_graph = 'src\graphs\helpers.py'
    graph_dimensions = extract_function_names(file_path_graph)

    return graph_dimensions

def graph_combined_types_kit(kit_id:int=0):
    # Graph Dimension
    file_path_graph = 'src\graphs\helpers.py'
    graph_dimensions = extract_function_names(file_path_graph)

    return graph_dimensions


def machine_algorithms_helper_kit(kit_id:int=0):
    # ML algorithms
    file_path_ml = 'src\Helpers\machine_learning_al\sklearnML.py'
    ml_algorithms = extract_function_names(file_path_ml)

    return ml_algorithms


def dimensionality_reduction_algorithms_helper_kit(kit_id:int=0):
    # DR algorithms
    file_path_dr = 'src\Helpers\machine_learning_al\dimensionality_reduction.py'
    dr_algorithms = extract_function_names(file_path_dr)

    return dr_algorithms


def normalization_algorithms_helper_kit(kit_id:int=0):
    # Normalization algorithms
    file_path_normal = 'src\Helpers\machine_learning_al\/normalization.py'
    normal_algorithms = extract_function_names(file_path_normal)
    return normal_algorithms



def graph_selection_categories_UI_kit(kit_id:int=0):
    options=["Date Fields", "Descriptions"]
    
    return options



def graph_group_by_date(kit_id:int = 0):
    dates_data = dates_columns
    # replace dot with underscore
    dates_data = tuple([str(s).replace('.', '_') for s in dates_data])
    return dates_data


def graph_group_by_others(kit_id:int = 0):
    desc = all_descriptors
    # replace dot with underscore
    desc = tuple([str(s).replace('.', '_') for s in desc])
    return desc


def date_grouping_methods(kit_id:int = 0):
    classes_options=["By Year", "By Month"]
    
    return classes_options

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
    return classes_options


def multi_select_kit(kit_id:int=0):
    select_options = ["single select", "multiple select"]
    return select_options

def quantification_fields_kit(kit_id:int=0, selection_type:str = "single select"):
    # Quantifications
    quantitative_data = cell_columns+rcsb_entries+quantitative_array_column

    return quantitative_data

def merge_graph_into_one_kit(kit_id:int=0):
    merge_graph_options = ["no", "yes"]
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

    return eps_slider, pca_features_slider, min_samples_slider, n_clusters_slider, n_components_slider