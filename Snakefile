
rule run_mpstruct_db_load:
    script:
        "serverConfig/DBFile.sh"

rule store_mpstruct_data:
    shell:
        "python manage.py init_migrate_mpstruct_upgrade"

rule store_pdb_data:
    shell:
        "python manage.py init_migrate_PDB_upgrade"
