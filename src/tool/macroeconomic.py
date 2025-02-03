import os
import requests
import traceback

from langchain.tools import tool

@tool(return_direct=False, parse_docstring=True, error_on_invalid_docstring=False)
def search_economic_data(series_id: str) -> dict:
    """
    Search for macroeconomic data from the FRED database.

    This tool retrieves economic data series using the FRED API, supporting various indicators
    such as GDP, inflation rates, unemployment, and other key economic metrics for different countries.

    Args:
        series_id (str): The FRED series ID for the economic indicator (e.g., 'GDP', 'UNRATE', 'CPIAUCSL').

    Returns:
        dict: A dictionary containing the last 6 data points for the requested economic indicator in JSON format.

    Raises:
        ValueError: If the FRED API key is not provided.

    Usage:
        - Use this function to fetch economic data like GDP, unemployment, inflation, etc., for the specified country.
        - This function returns only the last 6 available data points in JSON format.
    """
    api_key = os.getenv("FRED_API_KEY")

    if not api_key:
        raise ValueError("API key is required.")

    base_url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        observations = data.get("observations", [])
        
        # Return only the last 6 data points
        filtered_data = observations[-6:]
        
        return {"series_id": series_id, "last_6_data": filtered_data}
    else:
        print(f"Failed to fetch data: {traceback.format_exc()}")
        return {"error": f"Failed to fetch data: {response.status_code}"}