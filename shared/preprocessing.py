import pandas as pd
import os
from pathlib import Path

def clean_csv(file_path: str) -> pd.DataFrame:
    """
    Clean and preprocess CSV data with comprehensive cleaning steps.
    Returns a cleaned pandas DataFrame.
    """
    # Create cleaned_data directory if it doesn't exist
    cleaned_dir = Path(file_path).parent.parent / "cleaned_data"
    cleaned_dir.mkdir(exist_ok=True)
    
    # Read the original CSV
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    # 1. Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[\[\]()]", "", regex=True)
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    
    # 2. Clean string values
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    
    # 3. Handle missing values
    # For numeric columns, fill with median
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    
    # For categorical columns, fill with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])
    
    # 4. Remove duplicates
    df = df.drop_duplicates()
    
    # 5. Data type conversion
    # Convert ID columns to string
    id_cols = [col for col in df.columns if 'id' in col.lower()]
    for col in id_cols:
        df[col] = df[col].astype(str)
    
    # Convert numeric columns
    numeric_cols = [col for col in df.columns if any(term in col.lower() for term in ['count', 'number', 'amount', 'cost', 'price'])]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 6. Save cleaned version
    cleaned_path = cleaned_dir / f"cleaned_{Path(file_path).name}"
    df.to_csv(cleaned_path, index=False)
    
    return df
