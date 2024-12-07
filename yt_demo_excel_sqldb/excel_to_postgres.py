import pandas as pd
from sqlalchemy import create_engine, text, Integer, String, DECIMAL, MetaData, Table, Column
import sys
from pathlib import Path

def excel_to_postgres(excel_file='Sample-Sales-Data.xlsx', db_uri="postgresql://postgres:postgres@localhost:5432/testdb"):
    try:
        # Read the Excel file
        print(f"Reading Excel file: {excel_file}")
        df = pd.read_excel(excel_file)
        
        # Rename columns to match PostgreSQL naming convention (lowercase)
        df.columns = [col.lower() for col in df.columns]
        
        # Create SQLAlchemy engine
        print(f"Connecting to PostgreSQL database...")
        engine = create_engine(db_uri)
        
        # Create MetaData instance
        metadata = MetaData()
        
        # Define table structure
        sales_data = Table(
            'sales_data', 
            metadata,
            Column('postcode', Integer),
            Column('sales_rep_id', Integer),
            Column('sales_rep_name', String(100)),
            Column('year', Integer),
            Column('value', DECIMAL(12,2)),
        )
        
        # Create all tables
        print("Creating table structure...")
        metadata.drop_all(engine)  # Drop existing tables
        metadata.create_all(engine)
        
        # Create indexes using raw SQL for more control
        index_sql = """
        CREATE INDEX IF NOT EXISTS idx_sales_rep ON sales_data(sales_rep_id);
        CREATE INDEX IF NOT EXISTS idx_year ON sales_data(year);
        CREATE INDEX IF NOT EXISTS idx_postcode ON sales_data(postcode);
        """
        
        with engine.connect() as conn:
            # Create indexes
            print("Creating indexes...")
            conn.execute(text(index_sql))
            conn.commit()
            
            # Write the dataframe to PostgreSQL
            print("Writing data to PostgreSQL...")
            df.to_sql('sales_data', conn, if_exists='replace', index=False,
                     dtype={
                         'postcode': Integer,
                         'sales_rep_id': Integer,
                         'sales_rep_name': String(100),
                         'year': Integer,
                         'value': DECIMAL(12,2)
                     })
            
            # Get statistics
            print("\nGathering statistics...")
            
            # Total records
            result = conn.execute(text("SELECT COUNT(*) FROM sales_data"))
            row_count = result.scalar()
            
            # Unique sales reps
            result = conn.execute(text("SELECT COUNT(DISTINCT sales_rep_id) FROM sales_data"))
            sales_rep_count = result.scalar()
            
            # Year range
            result = conn.execute(text("SELECT MIN(year), MAX(year) FROM sales_data"))
            year_range = result.fetchone()
            
            print(f"\nMigration Summary:")
            print(f"- Total records: {row_count}")
            print(f"- Number of unique sales representatives: {sales_rep_count}")
            print(f"- Year range: {year_range[0]} to {year_range[1]}")
            
            # Sample analysis query
            print("\nSample data verification:")
            analysis_query = """
                SELECT 
                    sales_rep_name,
                    COUNT(*) as total_sales,
                    ROUND(SUM(value)::numeric, 2) as total_value,
                    ROUND(AVG(value)::numeric, 2) as avg_value
                FROM sales_data
                GROUP BY sales_rep_name
                LIMIT 3
            """
            
            result = conn.execute(text(analysis_query))
            for row in result:
                print(f"Sales Rep: {row[0]}")
                print(f"- Total Sales: {row[1]}")
                print(f"- Total Value: ${row[2]:,.2f}")
                print(f"- Average Value: ${row[3]:,.2f}")
            
            # Analyze table for query optimization
            print("\nOptimizing table statistics...")
            conn.execute(text("ANALYZE sales_data"))
            conn.commit()
            
        print("\nDatabase creation completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    excel_to_postgres()
