
rule run_mpstruct_db_load:
    shell: 
        "python ./src/jobs/MPStructJobs.py"

rule run_pdb_db_load:
    shell: 
        "python ./src/jobs/PDBJobs.py"

rule run_merge_db:
    shell: 
        "python ./src/jobs/MergeDB.py"

rule store_mpstruct_data:
    shell:
        "python manage.py init_migrate_mpstruct_upgrade"

rule store_pdb_data:
    shell:
        "python manage.py init_migrate_PDB_upgrade"
