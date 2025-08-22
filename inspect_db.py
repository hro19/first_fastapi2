"""
Database inspection script to discover existing tables and their structure.
"""
import sys
from sqlalchemy import inspect, MetaData, text
from sqlalchemy.orm import Session
from app.core.database import sync_engine
from app.core.config import settings
import json


def inspect_database():
    """Inspect the database and print all tables and their structure."""
    
    print(f"Connecting to database: {settings.DATABASE_NAME}")
    print("=" * 80)
    
    try:
        # Create inspector
        inspector = inspect(sync_engine)
        
        # Get all schema names
        schemas = inspector.get_schema_names()
        print(f"\nAvailable schemas: {schemas}")
        print("=" * 80)
        
        # Get all table names (default schema)
        table_names = inspector.get_table_names()
        print(f"\nTables in 'public' schema: {table_names}")
        print("=" * 80)
        
        # For each table, get detailed information
        for table_name in table_names:
            print(f"\n\nTable: {table_name}")
            print("-" * 40)
            
            # Get columns
            columns = inspector.get_columns(table_name)
            print("\nColumns:")
            for col in columns:
                col_type = str(col['type'])
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                default = f"DEFAULT {col['default']}" if col.get('default') else ""
                print(f"  - {col['name']}: {col_type} {nullable} {default}")
            
            # Get primary keys
            pk = inspector.get_pk_constraint(table_name)
            if pk['constrained_columns']:
                print(f"\nPrimary Key: {pk['constrained_columns']}")
            
            # Get foreign keys
            fks = inspector.get_foreign_keys(table_name)
            if fks:
                print("\nForeign Keys:")
                for fk in fks:
                    print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
            
            # Get indexes
            indexes = inspector.get_indexes(table_name)
            if indexes:
                print("\nIndexes:")
                for idx in indexes:
                    unique = "UNIQUE" if idx['unique'] else ""
                    print(f"  - {idx['name']}: {idx['column_names']} {unique}")
            
            # Get sample data (first 5 rows)
            with sync_engine.connect() as conn:
                result = conn.execute(text(f'SELECT * FROM "{table_name}" LIMIT 5'))
                rows = result.fetchall()
                if rows:
                    print(f"\nSample data (first {len(rows)} rows):")
                    # Get column names
                    col_names = result.keys()
                    print(f"  Columns: {list(col_names)}")
                    for i, row in enumerate(rows, 1):
                        print(f"  Row {i}: {dict(row._mapping)}")
                
                # Get row count
                count_result = conn.execute(text(f'SELECT COUNT(*) as count FROM "{table_name}"'))
                count = count_result.scalar()
                print(f"\nTotal rows: {count}")
        
        # Also check for views
        view_names = inspector.get_view_names()
        if view_names:
            print("\n" + "=" * 80)
            print(f"Views in 'public' schema: {view_names}")
            for view_name in view_names:
                print(f"\nView: {view_name}")
                columns = inspector.get_columns(view_name)
                for col in columns:
                    print(f"  - {col['name']}: {str(col['type'])}")
        
        # Check for custom types/enums
        with sync_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT n.nspname as schema, t.typname as type_name, 
                       array_agg(e.enumlabel ORDER BY e.enumsortorder) as enum_values
                FROM pg_type t 
                JOIN pg_namespace n ON n.oid = t.typnamespace 
                LEFT JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typtype = 'e' AND n.nspname = 'public'
                GROUP BY n.nspname, t.typname
            """))
            enums = result.fetchall()
            if enums:
                print("\n" + "=" * 80)
                print("Custom ENUM types:")
                for enum in enums:
                    print(f"  - {enum.type_name}: {enum.enum_values}")
        
        print("\n" + "=" * 80)
        print("Database inspection complete!")
        
    except Exception as e:
        print(f"Error inspecting database: {e}")
        print(f"Make sure your DATABASE_URL_SYNC in .env is correctly configured.")
        print(f"Current DATABASE_URL_SYNC: {settings.DATABASE_URL_SYNC[:50]}...")
        sys.exit(1)


if __name__ == "__main__":
    print("Starting database inspection...")
    print("Please make sure you have configured your .env file with the correct database credentials.")
    inspect_database()