import os
import re
import ast
import html
import json
import math
import inspect
import numpy as np
import pandas as pd
from flask import jsonify
import matplotlib.colors as mcolors
from src.services.data.columns.remove_columns import not_needed_columns

def convert_to_type(string_array):
    try:
        if string_array and not pd.isna(string_array):
            # Convert string array to numeric array
            value = ast.literal_eval(string_array)
        else:
            value = []
    except (Exception, ValueError, TypeError) as ex:
        value = []
    return value
    


def get_mean_value(value):
    try:
        data = convert_to_type(value)
        if (isinstance(value, (int, float))):
            average = 0
        else:
            average = sum(data) / len(data)
    except(Exception, ValueError, TypeError) as ex:
        average = 0
    return average

def extract_year(value):
    return pd.to_datetime(value, format='%b %d %Y').year
    # usage df["Year"] = df["date"].apply(extract_year)


def extract_function_names(file_path):
    function_names = []
    
    with open(file_path, 'r') as file:
        content = file.read()
        function_name_pattern = r'def\s+([\w_]+)\('
        matches = re.findall(function_name_pattern, content)
        # Remove __init__ if it exists in the list
        matches_list = [item for item in matches if item != '__init__']
        function_names.extend(matches_list)
    
    return function_names


def get_class_functions(class_instance):
    return [func for func, _ in inspect.getmembers(class_instance, inspect.ismethod)]


# Function to decode HTML entities
def decode_html_entities(text):
    return html.unescape(text)

def get_number(text):
    # Extract the number using regular expressions
    try:
        if(isinstance(text, (str))):
            number = re.findall(r'\d+(\.\d+)?', text)[0]
        else:
            number = text
        return number
    except (Exception, ValueError, TypeError) as ex:
        print(str(ex), text)


def group_by_year():
    pass


# Inject custom CSS to modify the color theme
def set_custom_theme():
    st.markdown(
        """
        <style>
        :root {
            --primary-color: #FF0000;  /* Replace with your desired color */
            --background-color: #F5F5F5;
        }
        .block-container{
            padding-top: 0px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def remove_default_side_menu():
    no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)


def does_file_exist(file_path):
    return os.path.exists(file_path)


def parser_change_dot_to_underscore(column_list:list = []):
    return [str(s).replace('.', '_') for s in column_list]


def is_date_valid_format(string):
    try:
        pd.to_datetime(string)
        return True
    except ValueError as ex:
        return False
    

def extract_year(bibliography):
    match = re.search(r"\['year', '(\d{4})'\]", bibliography)
    if match:
        return match.group(1)
    else:
        return None



#Convert month from 3-char string to respective number
def convert_month(mon):
    if (mon == "Jan"):
        return 1
    if (mon == "Feb"):
        return 2
    if (mon == "Mar"):
        return 3
    if (mon == "Apr"):
        return 4
    if (mon == "May"):
        return 5
    if (mon == "Jun"):
        return 6
    if (mon == "Jul"):
        return 7
    if (mon == "Aug"):
        return 8
    if (mon == "Sep"):
        return 9
    if (mon == "Oct"):
        return 10
    if (mon == "Nov"):
        return 11
    if (mon == "Dec"):
        return 12
    



#Strip the json strings and fix strings that would later become problematic (-> scottish names)
def prepare_column(df, column_name):
    table = df[column_name]
    table = table.replace(np.nan,"nan")
    ph = []
    for entry in table:
        entry = str(entry)
        ph_2 = entry.replace("[","")
        ph_3 = ph_2.replace("]","")
        ph_4 = ph_3.replace("\'", "\"")
        ph_41 = ph_4.replace("O\"C","OC")
        ph_42 = ph_41.replace("O\"D","OD")
        ph_5 = ph_42.split("},")

        ph_ls = []
        for one_ph in ph_5:
            if ((one_ph) != "nan"):
                ph5_len = len(ph_5)-1
                if (ph_5.index(one_ph) != ph5_len):
                    ph_ls.append(one_ph + "}")
                else:
                    ph_ls.append(one_ph)
                    
        ph.append(ph_ls)
        
    return ph


#Strip the specific entries
def strip_entry(column_entry):
    column_entry = str(column_entry)
    column_entry = column_entry.replace("[","")
    column_entry = column_entry.replace("]","")
    column_entry = column_entry.replace("\'", "")
    column_entry = column_entry.replace("{", "")
    column_entry = column_entry.replace("}", "")
    column_entry = column_entry.replace("\"", "")
    column_entry = column_entry.replace(",", "")
    column_entry = html.unescape(column_entry)
    
    column_entry = column_entry.split()
    
    return column_entry


#Find the key-value pairs within the strings and save them as paired lists
def find_kv_pairs(stripped_list):
    
    paired_list = []
    
    keys = []
    for one_entry in stripped_list:
        if (one_entry.find(":") != -1):
            keys.append(one_entry)
            
    for i in range(len(keys)):
        one_pair = []
        j = stripped_list.index(keys[i])
        if (i < len(keys)-1):
            while (j < stripped_list.index(keys[i+1])):
                one_pair.append(stripped_list[j])
                j += 1
        else:
            while (j <= len(stripped_list)-1):
                one_pair.append(stripped_list[j])
                j += 1            
        paired_list.append(one_pair)    
            
        
    return paired_list



#KIND OF OPTIONAL: save the paired lists as a string, separating elements with semicolon
def finalize_entry(paired_list):
    
    output_string = ""
    
    for one_entry in paired_list:
        for one_element in one_entry:
            output_string += one_element + " "
        if (paired_list.index(one_entry) != len(paired_list)-1):
            output_string += "; "
            
    return output_string 




#Apply all above functions to a given column based on the number of elements in each entry
def work_column(prepared_column):
    
    finished_column = []
    
    if (len(prepared_column) == 1):
        for one_entry in prepared_column:
            finished_entry = finalize_entry(find_kv_pairs(strip_entry(one_entry)))
            finished_column.append(finished_entry)
    elif (len(prepared_column) > 1):
        for one_entry_list in prepared_column:
            finished_entries = []
            for one_entry in one_entry_list:
                finished_entry = finalize_entry(find_kv_pairs(strip_entry(one_entry)))
                finished_entries.append(finished_entry)
            finished_column.append(finished_entries)
    
    return finished_column




# Function to check if a value is empty
def can_be_processed(value):
    if isinstance(value, str):
        return value.strip() != ''  # Check if string is not empty
    elif isinstance(value, (list, np.ndarray)):
        return len(value) > 0  # Check if list/array is not empty
    else:
        return False  # Value is not empty if it's neither a string nor a list/array



# Function to check if a value is empty
def preprocess_data(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, (list, np.ndarray)):
        if (len(value) > 1):
           return value
        else:
            # strip off []
            return value.strip('[]')
        return len(value) > 0  # Check if list/array is not empty
    else:
        return value


# Function to check if a string of list dictionaries is not empty
def preprocess_str_data(str_value):
    try:
        # Parse the string into a list of dictionaries using ast.literal_eval
        value_list = ast.literal_eval(str_value)
        if(isinstance(value_list, list) and len(value_list) > 1):
            # then take the first on the list 
            new_str = ast.literal_eval([value_list[0]])
            return new_str
        else:
            return ast.literal_eval(str_value.strip('[]'))
    except (SyntaxError, ValueError):
        return {}
    
def str_can_be_processed(str_value):
    try:
        # Parse the string into a list of dictionaries using ast.literal_eval
        value_list = ast.literal_eval(str_value)
        if(isinstance(value_list, list) and len(value_list) >= 1):
            return True
    except (SyntaxError, ValueError):
        return False
    

def NAPercent(df):
    NA = pd.DataFrame(data=[df.isna().sum().tolist(), [i \
           for i in (df.isna().sum()/df.shape[0]*100).tolist()]], 
           columns=df.columns, index=['NA Count', 'NA Percent']).transpose()

    return NA 



def get_key_from_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None  



def remove_bad_columns(df):
    # Remove unnamed columns from the list.
    columns = not_needed_columns
    df = df.drop(columns, inplace=False, axis=1)
    return df


def round_to_2dp(value):
    return math.ceil(value * 100) / 100

def generate_range_bins(range_resolution, max_range):
    num_bins = int(max_range / range_resolution)
    range_bins = [(round_to_2dp(i * range_resolution), round_to_2dp((i + 1) * range_resolution)) for i in range(num_bins)]
    range_bins_str = [f"{item[0]}-{item[1]}" for item in range_bins]
    return range_bins_str

def generate_list_with_difference(num_elements, difference):
    result_list = [round_to_2dp(i * difference) for i in range(num_elements)]
    return result_list


# Custom function to convert string numbers to numeric values
def convert_to_numeric_or_str(value):
    if(value and value != " "):
        try:
            return float(value)
        except (ValueError, KeyError):
            try:
                return float(value)
            except (ValueError, KeyError):
                return value
        


# Function to remove all HTML tags from a string
def remove_html_tags(text):
    try:
        if not text is None and pd.notna(text):
            clean_text = re.sub(r'<.*?>', '', text)
            # Replace '\r' and '\n' with a space
            clean_text = clean_text.replace('\r', ' ').replace('\n', ' ')
            return clean_text
        else:
            return ''
    
    except (Exception, TypeError) as e:
        print(str(e))


def remove_underscore_change_toupper(original_string):
    return original_string.replace("_", " ").upper()


def replace_and_separate(text):
    # Define the regex patterns for matching the substrings to replace
    patterns = [
        r'^pdbx_serial_',
        r'^pdbx_nmr_'
        r'^pdbx_database_status_',
        r'^pdbx_nmr_ensemble_',
        r'^rcsb_primary_citation_rcsb_',
        r'^rcsb_primary_citation_rcsb_'
    ]

    # Replace the substrings with 'pdbx' or 'rcsb'
    try:
        for pattern in patterns:
            text = re.sub(pattern, 'pdbx_' if pattern.startswith('^pdbx') else 'rcsb_', text)
    except (Exception, TypeError, ValueError) as e:
        print(e)

    return text
    

def filter_list(item_list, ends_with):
    result = list(filter(lambda item: item.endswith(ends_with), item_list))
    return result

def format_string_caps(input_string):
    # Replace underscores with spaces
    formatted_string = input_string.replace('_', ' ')
    
    # Capitalize the first character
    formatted_string = formatted_string.capitalize()

    return formatted_string


"""
    Converter for the basic statistics selection
    This method helps us to match the text selected
    to the list item or if doesn't exist as text then we 
    want to assume the key was used.
"""
from src.Dashboard.data import stats_data
def summaryStatisticsConverter(search_key):
    # get content of data in each object
    data = []
    for d in stats_data():
        data += d['data']

    found_key = ""

    # Check if the name exists directly in the values
    for entry in data:
        print(search_key +"=="+ entry['value'])
        if search_key == entry['value']:
            content_value = entry['value']
            found_key = content_value
            break
    else:
        # If not found, check the name in the name attributes
        for entry in data:
            if search_key == entry['name']:
                content_value = entry['value']
                found_key = content_value
                break
        else:
            found_key = ""

    return stats_data(), data, found_key

"""
    return a simple list of summary statistics options rather
    than complex dataset for filter.
"""

def summaryStatisticsFilterOptions():
    merged_list = [data for d in stats_data() for data in d["data"].values()]

    return merged_list


def removeUnderscoreIDFromList(_list):
    cleaned_list = [item for item in _list if not item.endswith("_id") and not item.endswith("_id_pub_med")]
    return cleaned_list


def tableHeader(header_list:list = []):
    list_of_objects = [
        {'id': i, 'text': format_string_caps(item), 'value': item, "sortable": True} for i, item in enumerate(header_list, start=1)
    ]

    return list_of_objects



def create_json_response(httpResponse=False, data=None, status=None, status_code=200, message=None, error_message=None, extras=None):
    response_data = {'status_code': status_code}
    
    if data is not None:
        response_data['data'] = data
    if message is not None:
        response_data['message'] = message
    if status is not None:
        response_data['status'] = status
    if error_message is not None:
        response_data['error_message'] = error_message
    if extras is not None:
        response_data.update(extras)
    
    if(httpResponse):
        response = jsonify(response_data)
        response.status_code = status_code
    else:
        response = response_data

    return response

def convert_json_to_dict(json_response):
    return json.loads(json_response)


def find_dict_with_value_in_nested_data(array_of_dicts, search_value):
    for data_dict in array_of_dicts:
        for inner_dict in data_dict["data"]:
            if inner_dict["value"] == search_value:
                return data_dict
    return None



def generate_color_palette(start_color, end_color, num_colors):
    # Convert hex colors to RGB
    start_rgb = mcolors.hex2color(start_color)
    end_rgb = mcolors.hex2color(end_color)

    # Create a list of RGB colors in the gradient
    colors = []
    for i in range(num_colors):
        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (i / (num_colors - 1))
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (i / (num_colors - 1))
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (i / (num_colors - 1))
        colors.append((r, g, b))

    # Convert RGB colors back to hex
    hex_colors = [mcolors.rgb2hex(color) for color in colors]

    return hex_colors


    # USAGE: # Define the start and end hex colors
    # start_color = '#005EB8'  # Red
    # end_color = '#B87200'    # Green

    # # Generate a color palette with 10 colors
    # num_colors = 5
    # palette = generate_color_palette(start_color, end_color, num_colors)
    # print(palette)
    # # Display the color palette
    # fig, ax = plt.subplots(figsize=(8, 2))
    # cmap = mcolors.ListedColormap(palette)
    # cax = ax.matshow([[i] for i in range(num_colors)], cmap=cmap)
    # plt.xticks([])  # Hide x-axis labels
    # plt.yticks([])  # Hide y-axis labels
    # plt.show()

    # # Print the hex colors in the palette
    # print(palette)


import ast
def get_class_names(file_path):
    class_names = []
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_names.append(node.name)

    return class_names