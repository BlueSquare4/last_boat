import pandas as pd
import requests
import io

# The URL from PS.md
# https://docs.google.com/spreadsheets/d/1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VE E/edit?gid=1438203274#gid=1438203274
# Fixing the potential typo in URL if needed, but assuming standard export format.
# A safe way to get CSV from GSheet is replacing /edit... with /export?format=csv
SHEET_ID = "1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VE" # Hypothetical ID if URL was standard
# Let's try to use the direct export URL pattern
SHEET_URL = "https://docs.google.com/spreadsheets/d/1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VE/export?format=csv&gid=1438203274"

def load_seo_data() -> pd.DataFrame:
    """Loads the SEO data from the provided Google Sheet."""
    try:
        response = requests.get(SHEET_URL)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        return df
    except Exception as e:
        # Fallback or error handling
        print(f"Failed to load sheet: {e}")
        return pd.DataFrame()

def query_seo_data(sql_like_query: str = None) -> str:
    """
    Queries the SEO audit data.
    The agent can check for issues like missing meta tags, status codes, logic, etc.
    
    Args:
        sql_like_query (optional): description of filter intent, e.g. "Address contains http"
                                     Currently, we usually implement specific filters, 
                                     but for this tool we'll return a sample or summary if no specific complex logic is built yet.
                                     For a real powerful agent, we might use pandas query or just return the head.
    
    For best results, the LLM should ask for specific columns or filtering logic.
    Since we cannot execute arbitrary SQL safely easily without a library, 
    we will provide a tool that returns a JSON summary or supports basic filtering filters.
    """
    df = load_seo_data()
    
    # Simple logic: if specific column requested, return it.
    # For now, let's return a summary of columns and the first 5 rows
    # so the LLM can see what's available and then we can add a 'filter_data' tool.
    
    info = {
        "columns": list(df.columns),
        "total_rows": len(df),
        "sample": df.head(5).to_dict(orient='records')
    }
    return json.dumps(info, default=str)

import json

def filter_seo_data(column: str, operator: str, value: str) -> str:
    """
    Filters the SEO dataset.
    
    Args:
        column: The column name to filter on (e.g., 'Status Code', 'Title 1', 'Address').
        operator: 'equals', 'contains', 'gt' (greater than), 'lt' (less than).
        value: The value to compare against.
    """
    df = load_seo_data()
    
    if column not in df.columns:
        return f"Error: Column '{column}' not found. Available: {list(df.columns)}"
        
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
            return "Error: Unknown operator. Use equals, contains, gt, lt."
            
        return json.dumps(result.head(20).to_dict(orient='records'), default=str)
    except Exception as e:
        return f"Error filtering data: {str(e)}"
