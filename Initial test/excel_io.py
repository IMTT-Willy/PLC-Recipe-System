import pandas as pd

def load_recipe(filepath):
    df = pd.read_excel(filepath)
    if not {'Address', 'Value'}.issubset(df.columns):
        raise ValueError("Excel file must contain 'Address' and 'Value' columns")
    return [(str(row['Address']), int(row['Value'])) for _, row in df.iterrows()]