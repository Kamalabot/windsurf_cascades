import pandas as pd
import sys
from pathlib import Path

def excel_to_csv(excel_file='SaleData.xlsx', csv_file=None):
    try:
        # If no CSV filename is provided, use the Excel filename with .csv extension
        if csv_file is None:
            csv_file = Path(excel_file).stem + '.csv'
        
        print(f"Reading Excel file: {excel_file}")
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Convert to CSV
        print(f"Converting to CSV: {csv_file}")
        df.to_csv(csv_file, index=False)
        
        # Get file sizes for comparison
        excel_size = Path(excel_file).stat().st_size
        csv_size = Path(csv_file).stat().st_size
        
        # Print summary
        print("\nConversion Summary:")
        print(f"- Excel file size: {excel_size:,} bytes")
        print(f"- CSV file size: {csv_size:,} bytes")
        print(f"- Number of rows: {len(df):,}")
        print(f"- Number of columns: {len(df.columns):,}")
        print("\nColumn names:")
        for col in df.columns:
            print(f"- {col}")
            
        print(f"\nCSV file created successfully: {csv_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    excel_to_csv()
