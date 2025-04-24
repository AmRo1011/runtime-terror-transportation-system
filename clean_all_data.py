from shared.data_loader import DATA_PATHS
from shared.preprocessing import clean_csv
import os

def clean_all_data():
    print("Starting data cleaning process...")
    
    for data_type, file_path in DATA_PATHS.items():
        print(f"\nCleaning {data_type} data...")
        try:
            # Clean the data and save to cleaned_data directory
            df = clean_csv(file_path)
            print(f"Successfully cleaned {data_type} data")
            print(f"Original shape: {df.shape}")
        except Exception as e:
            print(f"Error cleaning {data_type}: {str(e)}")
    
    print("\nData cleaning completed!")

if __name__ == "__main__":
    clean_all_data() 