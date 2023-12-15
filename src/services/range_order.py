
from src.Commands.migrateCommandMPstruct import shorten_column_name


columns_range_limit = {
    'Resolution': 2,
    'rcsb_entry_info_deposited_atom_count': 1000,
    'refine_hist_pdbx_number_residues_total': 100,
    'citation_year': 5,
}

def reduce_key_length_in_dict(data_dict):
    new_dict = {}
    for key, value in data_dict.items():
        new_key = shorten_column_name(key) if isinstance(key, str)  else key
        new_dict[new_key] = value
    return new_dict


columns_range_limit = reduce_key_length_in_dict(columns_range_limit)