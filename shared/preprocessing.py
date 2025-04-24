
import pandas as pd

def clean_csv(path: str) -> pd.DataFrame:
    """Reads and cleans a CSV file by standardizing headers and stripping whitespace."""
    df = pd.read_csv(path, encoding='utf-8-sig')

    # Clean headers
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[\[\]()]", "", regex=True)
        .str.replace(" ", "-", regex=False)
        .str.replace("_", "-", regex=False)
    )

    # Clean string values
    df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x) if col.dtypes == "object" else col)


    return df
