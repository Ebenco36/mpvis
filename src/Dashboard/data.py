"""
    This method provides data filter for our basic summary statistics
    @return list
    Param None
"""
def stats_data():
    data = []
    # trying to group these sections accordingly.
    data.append({
        "section": 'data_distribution', 
        "data": [
            {
                "value" : "rcsb_entry_info_selected_polymer_entity_types", 
                "name"  : "by Experimental Method and Molecular Type"
            },
            {
                "value" : "Species", 
                "name"  : "by Natural Source Organism"
            },
            {
                "value" : "Species", 
                "name"  : "by Engineered Source Organism"
            },
            {
                "value" : "Expressed in Species", 
                "name"  : "by Expression System Organism"
            },
            {
                "value" : "Resolution", 
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
    })

    data.append({
        "section": 'released_structure_per_year', 
        "data": [
            {
                "value" : "sdds", 
                "name"  : "Overall"
            },
            {
                "value" : "rcsb_entry_info_experimental_method-xray", 
                "name"  : "by X-ray",
            },
            {
                "value" : "rcsb_entry_info_experimental_method-nmr", 
                "name"  : "by NMR",
            },
            {
                "value" : "rcsb_entry_info_experimental_method-EM", 
                "name"  : "by Electron Microscopy",
            },
            {
                "value" : "rcsb_entry_info_experimental_method-MM", 
                "name"  : "by Multi-method",
            },
            {
                "value" : "rcsb_entry_info_experimental_method-ProteinOnly", 
                "name"  : "by Protein-only",
            },
            {
                "value" : "rcsb_entry_info_experimental_method-PNAC", 
                "name"  : "by Protein-Nucleic Acid Complexes",
            },
            {
                "value" : "rcsb_entry_info_experimental_method-AS", 
                "name"  : "by Assembly Symmetry",
            }
        ]
    })

    return data


def array_string_type ():
    array_list = ['rcsb_entry_info_software_programs_combined', ]

    return array_list