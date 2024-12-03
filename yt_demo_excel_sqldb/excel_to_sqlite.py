import pandas as pd
import sqlite3
from pathlib import Path

def excel_to_sqlite(excel_file='Sample-Sales-Data.xlsx', db_name='sales_database.db'):
    try:
        # Read the Excel file
        print(f"Reading Excel file: {excel_file}")
        df = pd.read_excel(excel_file)
        
        # Create SQLite connection
        print(f"Creating/connecting to SQLite database: {db_name}")
        conn = sqlite3.connect(db_name)
        
        # Create the table with specific data types
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS sales_data (
            postcode INTEGER,
            sales_rep_id INTEGER,
            sales_rep_name TEXT,
            year INTEGER,
            value REAL,
            PRIMARY KEY (sales_rep_id, postcode, year)
        )
        """
        conn.execute(create_table_sql)
        
        # Write the dataframe to SQLite
        print("Writing data to SQLite...")
        df.to_sql('sales_data', conn, if_exists='replace', index=False,
                  dtype={
                      'Postcode': 'INTEGER',
                      'Sales_Rep_ID': 'INTEGER',
                      'Sales_Rep_Name': 'TEXT',
                      'Year': 'INTEGER',
                      'Value': 'REAL'
                  })
        
        # Create indexes for better query performance
        print("Creating indexes...")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_rep ON sales_data(sales_rep_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_year ON sales_data(year)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_postcode ON sales_data(postcode)")
        
        # Get some statistics
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales_data")
        row_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT sales_rep_id) FROM sales_data")
        sales_rep_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT MIN(year), MAX(year) FROM sales_data")
        year_range = cursor.fetchone()
        
        print(f"\nMigration Summary:")
        print(f"- Total records: {row_count}")
        print(f"- Number of unique sales representatives: {sales_rep_count}")
        print(f"- Year range: {year_range[0]} to {year_range[1]}")
        
        # Sample query to verify data
        print("\nSample data verification:")
        cursor.execute("""
            SELECT 
                sales_rep_name,
                COUNT(*) as total_sales,
                ROUND(SUM(value), 2) as total_value,
                ROUND(AVG(value), 2) as avg_value
            FROM sales_data
            GROUP BY sales_rep_name
            LIMIT 3
        """)
        sample_data = cursor.fetchall()
        for row in sample_data:
            print(f"Sales Rep: {row[0]}")
            print(f"- Total Sales: {row[1]}")
            print(f"- Total Value: ${row[2]:,.2f}")
            print(f"- Average Value: ${row[3]:,.2f}")
        
        conn.close()
        print("\nDatabase creation completed successfully!")
        
    except FileNotFoundError:
        print(f"Error: The Excel file '{excel_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Check if Excel file exists
    excel_file = "Sample-Sales-Data.xlsx"
    if not Path(excel_file).exists():
        print(f"\nWarning: {excel_file} not found in the current directory!")
        print("Please ensure your Excel file is in the same directory as this script.")
        print("Expected Excel file format should have columns like:")
        print("- Order ID")
        print("- Product")
        print("- Quantity")
        print("- Price")
        print("- Customer")
        print("- Date")
        print("(The actual column names may vary based on your data)")
    else:
        excel_to_sqlite()
