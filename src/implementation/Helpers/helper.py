import pandas as pd
import ast
import os
import re
import html
import math
import numpy as np
from bs4 import BeautifulSoup
from src.implementation.data.columns.remove_columns import not_needed_columns

def convert_to_type(string_array):
    try:
        # Convert string array to numeric array
        value = ast.literal_eval(string_array)
    except (Exception, ValueError, TypeError) as ex:
        value = 0
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
        
        function_names.extend(matches)
    
    return function_names


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
def prepare_column(column_name):
    table = pdb_table[column_name]
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
    print(num_elements)
    result_list = [round_to_2dp(i * difference) for i in range(num_elements)]
    return result_list


# Custom function to convert string numbers to numeric values
def convert_to_numeric_or_str(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
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
        print(text)
        print(str(e))


def remove_underscore_change_toupper(original_string):
    return original_string.replace("_", " ").upper()