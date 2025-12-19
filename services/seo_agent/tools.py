import pandas as pd
import requests
import io
import json

# Google Sheets export URL for SEO data
SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"

def load_seo_data() -> pd.DataFrame:
    """Loads SEO data from Google Sheets."""
    try:
        response = requests.get(SHEET_URL, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        return df
    except Exception as e:
        print(f"Failed to load sheet: {e}")
        return pd.DataFrame()

def query_seo_data() -> str:
    """Returns schema and sample of SEO data."""
    df = load_seo_data()
    
    if df.empty:
        return json.dumps({"error": "No data available", "columns": []})
    
    return json.dumps({
        "columns": list(df.columns),
        "total_rows": len(df),
        "sample": df.head(5).to_dict(orient='records')
    }, default=str)

def filter_seo_data(column: str, operator: str, value: str) -> str:
    """Filters SEO dataset by column and operator."""
    df = load_seo_data()
    
    if df.empty:
        return json.dumps({"error": "No data available"})
    
    if column not in df.columns:
        return json.dumps({"error": f"Column '{column}' not found. Available: {list(df.columns)}"})
    
    try:
        if operator == 'equals':
            result = df[df[column].astype(str) == str(value)]
        elif operator == 'contains':
            result = df[df[column].astype(str).str.contains(str(value), case=False, na=False)]
        elif operator == 'gt':
            result = df[pd.to_numeric(df[column], errors='coerce') > float(value)]
        elif operator == 'lt':
            result = df[pd.to_numeric(df[column], errors='coerce') < float(value)]
        else:
            return json.dumps({"error": "Unknown operator. Use: equals, contains, gt, lt"})
        
        return json.dumps(result.head(20).to_dict(orient='records'), default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
