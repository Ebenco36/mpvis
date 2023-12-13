"""
    This method provides data filter for our basic summary statistics
    @return list
    Param None
"""
from src.Commands.migrateCommandMPstruct import shorten_column_name


def stats_data(for_processing=True):
    data = []
    # trying to group these sections accordingly.
    section1 = [
        {
            "value" : "rcsb_entry_info_selected_polymer_entity_types", 
            "name"  : "by Experimental Method and Molecular Type"
        },
        {
            "value" : "species", 
            "name"  : "by Natural Source Organism"
        },
        {
            "value" : "species", 
            "name"  : "by Engineered Source Organism"
        },
        {
            "value" : "expressed in species", 
            "name"  : "by Expression System Organism"
        },
        {
            "value" : "resolution", 
            "name"  :  "by Resolution"
        },
        {
            "value" : "rcsb_entry_info_software_programs_combined", 
            "name"  : "by Software"
        },
        {
            "value" : "refine_ls_rfactor_rfree", 
            "name"  :  "by R-free"
        },
        {
            "value" : "symmetry_space_group_name_hm", 
            "name"  : "by Space Group"
        },
        {
            "value" : "rcsb_primary_citation_journal_abbrev", 
            "name"  :  "by Journal"
        },
        {
            "value" : "rcsb_entry_info_molecular_weight", 
            "name"  :  "by Molecular Weight (Structure)"
        },
        {
            "value" : "rcsb_entry_info_molecular_weight", 
            "name"  :  "by Molecular Weight (Entity)"
        },
        {
            "value" : "rcsb_entry_info_deposited_atom_count", 
            "name"  :  "by Atom Count"
        },
        {
            "value" : "rcsb_entry_info_deposited_atom_count", 
            "name"  :  "by Residue Count"
        },
        {
            "value" : "pdbx_sgproject_full_name_of_center", 
            "name"  :  "by Structural Genomics Centers"
        },
    ]
    section2 = [
        {
            "value" : "rcsb_entry_info_experimental_method", 
            "name"  : "Overall"
        },
        {
            "value" : "rcsb_entry_info_experimental_method*X-ray", 
            "name"  : "by X-ray",
        },
        {
            "value" : "rcsb_entry_info_experimental_method*NMR", 
            "name"  : "by NMR",
        },
        {
            "value" : "rcsb_entry_info_experimental_method*EM", 
            "name"  : "by Electron Microscopy",
        },
        {
            "value" : "rcsb_entry_info_experimental_method*Multiple methods", 
            "name"  : "by Multi-method",
        },
        {
            "value" : "rcsb_entry_info_selected_polymer_entity_types*Protein (only)", 
            "name"  : "by Protein-only",
        },
        {
            "value" : "rcsb_entry_info_selected_polymer_entity_types*Protein/NA", 
            "name"  : "by Protein-Nucleic Acid Complexes",
        },
        # {
        #     "value" : "rcsb_entry_info_experimental_method*AS", 
        #     "name"  : "by Assembly Symmetry",
        # },
        {
            "value" : "rcsb_entry_info_experimental_method", 
            "name"  : "By Methods"
        }
    ]
    
    if(not for_processing):
        section1 = reduce_value_length(section1)
        section2 = reduce_value_length(section2)
    
    data.append({
        "section": 'data_distribution', 
        "data": section1
    })

    data.append({
        "section": 'released_structure_per_year', 
        "data": section2
    })


    return data


def array_string_type ():
    array_list = ['rcsb_entry_info_software_programs_combined', ]

    return array_list


def reduce_value_length(data):
    for item in data:
        if 'value' in item:
            item['value'] = shorten_column_name(item['value'])
    return data