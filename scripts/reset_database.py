"""
Reset all database tables: delete data and reset ID sequences to 1
Run this script to clear the database and start fresh with ID sequences from 1
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text, inspect
from app.database import engine
# Import models to ensure they're registered
from app import models

def reset_database():
    """Delete all data from all tables and reset sequences to start from 1."""
    
    with engine.connect() as connection:
        # Get all tables from the database
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        
        print(f"Found {len(table_names)} tables to process...")
        
        # Disable foreign key constraints temporarily
        connection.execute(text("SET session_replication_role = 'replica'"))
        
        # Delete all data from each table and reset sequences
        for table_name in sorted(table_names):
            if table_name.startswith('pg_'):  # Skip PostgreSQL internal tables
                continue
            
            try:
                # Truncate the table (delete all data)
                connection.execute(text(f'TRUNCATE TABLE "{table_name}" CASCADE'))
                print(f"✓ Truncated {table_name}")
                
                # Reset sequence to 1
                sequence_names = inspector.get_pk_constraint(table_name)
                if sequence_names['constrained_columns']:
                    # Get the first primary key column
                    pk_col = sequence_names['constrained_columns'][0]
                    # The sequence name is typically table_column_seq
                    seq_name = f"{table_name}_{pk_col}_seq"
                    try:
                        connection.execute(text(f'ALTER SEQUENCE "{seq_name}" RESTART WITH 1'))
                        print(f"  └─ Reset sequence {seq_name} to 1")
                    except Exception as e:
                        print(f"  └─ No sequence to reset for {table_name} (or already handles IDs)")
            except Exception as e:
                print(f"✗ Error processing {table_name}: {str(e)}")
        
        # Re-enable foreign key constraints
        connection.execute(text("SET session_replication_role = 'origin'"))
        connection.commit()
        
        print("\n✓ Database reset complete! All tables are empty and ID sequences start from 1.")

if __name__ == "__main__":
    reset_database()
