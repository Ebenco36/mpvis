from datetime import datetime
from database.db import db

class MPSTURCT(db.Model):
    __tablename__ = 'membrane_protein_mpstruct'
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String)
    subgroup = db.Column(db.String)
    pdb_code = db.Column(db.String)
    is_master_protein = db.Column(db.String)
    name = db.Column(db.String)
    species = db.Column(db.String)
    taxonomic_domain = db.Column(db.String)
    expressed_in_species = db.Column(db.String)
    resolution = db.Column(db.String)
    description = db.Column(db.String)
    bibliography = db.Column(db.String)
    secondary_bibliogrpahies = db.Column(db.String)
    related_pdb_entries = db.Column(db.String)
    member_proteins = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
