from flask import abort, send_file
import pandas as pd
from sqlalchemy import func
from database.db import db
from sqlalchemy import select, func, desc
from sqlalchemy import text
from sqlalchemy.sql import select
from sqlalchemy.orm import Query
from sqlalchemy import or_
from src.MP.model import MembraneProteinData
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

def get_all_items():
    return MembraneProteinData.query


# Function to apply search and filter
def apply_search_and_filter(query, search_term):
    if search_term:
        # Perform case-insensitive search on 'name' and 'description' columns
        query = query.filter(or_(
            MembraneProteinData.name.ilike(f"%{search_term}%"),
            MembraneProteinData.pdb_code.ilike(f"%{search_term}%")
        ))
    return query

# Function to apply sorting
def apply_sorting(query, sort_by, sort_order):
    if sort_by:
        # Sort by the specified column and order
        column = getattr(MembraneProteinData, sort_by)
        query = query.order_by(column.asc() if sort_order.lower() == 'asc' else column.desc())
    return query


def get_items(request):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    search_term = request.args.get('search_term', default='', type=str)
    sort_by = request.args.get('sort_by', default='id', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)
    download = request.args.get('download', default='none', type=str)

    items = get_all_items()
    
    # Apply search and filter
    items = apply_search_and_filter(items, search_term)

    # Apply sorting
    items = apply_sorting(items, sort_by, sort_order)
    
    if (download in ["csv", "xlsx"]):
        # Retrieve all records after applying the filter
        filtered_records = items.all()

        # Get column names dynamically
        column_names = [desc for desc in items.statement.columns.keys()]
        # Convert records to a DataFrame
        records_df = pd.DataFrame([{col: getattr(record, col) for col in column_names} for record in filtered_records])
        
        return records_df
        

    # Perform pagination using LIMIT and OFFSET
    paginated_items = items.paginate(page=page, per_page=per_page, error_out=False)

    # Extract items and metadata
    items_list = [{
        'id': item.id, 
        'name': item.name,
        'group': item.group,
        'species': item.species,
        'subgroup': item.subgroup,
        'pdb_code': item.pdb_code,
        'resolution': item.resolution,
        'exptl_method': item.exptl_method,
        'taxonomic_domain': item.taxonomic_domain,
        'expressed_in_species': item.expressed_in_species,
        'rcsentinfo_experimental_method': item.rcsentinfo_experimental_method
    } for item in paginated_items.items]
    result = {
        'items': items_list,
        'page': paginated_items.page,
        'per_page': paginated_items.per_page,
        'total_items': paginated_items.total,
        'total_pages': paginated_items.pages,
        'total_columns': len(MembraneProteinData.__table__.columns),
        'total_rows': items.count() 
    }
    
    return result


def get_table_as_dataframe(table_name):
    # Reflect the table using SQLAlchemy
    table = db.Table(table_name, db.metadata, autoload_with=db.engine)
    
    # Create a SQLAlchemy SELECT query
    query = db.select([table])

    # Execute the query using the db session and fetch all results
    result = db.session.execute(query)
    records = result.fetchall()

    # Create a list of dictionaries from the query result
    records_dict = [dict(record) for record in records]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(records_dict)

    return df
    


class PaginatedQuery(Query):
    def paginate(self, page, per_page=10, error_out=True):
        if error_out and page < 1:
            abort(404)

        items = self.limit(per_page).offset((page - 1) * per_page).all()
        total = self.order_by(None).count()

        return {'items': items, 'total': total, 'page': page, 'per_page': per_page}

# Apply the PaginatedQuery to the SQLAlchemy session
db.session.query_class = PaginatedQuery

def get_table_as_dataframe_exception(table_name, filter_column=None, filter_value=None, page=1, per_page=10):
    page = int(page)
    per_page = int(per_page)
    # Reflect the table using SQLAlchemy
    table = db.Table(table_name, db.metadata, autoload_with=db.engine)

    # Create a SQLAlchemy SELECT query
    query = select([table])

    # Add a filter condition if provided
    if filter_column and filter_value:
        query = query.where(getattr(table.columns, filter_column) == filter_value)

    # Execute the query using the db session
    result = db.session.execute(query.limit(per_page).offset((page - 1) * per_page))

    # Fetch the paginated result as a list
    paginated_data = result.fetchall()

    # Convert the paginated result to a DataFrame
    df = pd.DataFrame(paginated_data, columns=result.keys())

    # Calculate the total_rows separately
    total_rows = db.session.execute(select([func.count()]).select_from(table).where(getattr(table.columns, filter_column) == filter_value)).scalar()

    return {'data': df.to_dict(orient='records'), 'total_rows': total_rows, 'page': page, 'per_page': per_page}


def get_table_as_dataframe_download(table_name, filter_column=None, filter_value=None):
    # Reflect the table using SQLAlchemy
    table = db.Table(table_name, db.metadata, autoload_with=db.engine)

    # Create a SQLAlchemy SELECT query
    query = select([table])

    # Add a filter condition if provided
    if filter_column and filter_value:
        query = query.where(getattr(table.columns, filter_column) == filter_value)

    # Execute the query using the db session
    result = db.session.execute(query)

    # Fetch all the data
    all_data = result.fetchall()

    # Convert the result to a DataFrame
    df = pd.DataFrame(all_data, columns=result.keys())

    # Calculate the total_rows separately
    total_rows = db.session.execute(select([func.count()]).select_from(table).where(getattr(table.columns, filter_column) == filter_value)).scalar()

    return {'data': df, 'total_rows': total_rows}

def export_to_csv(df, csv_filename):
    df.to_csv(csv_filename, index=False)

def export_to_excel(df, excel_filename):
    df.to_excel(excel_filename, index=False)