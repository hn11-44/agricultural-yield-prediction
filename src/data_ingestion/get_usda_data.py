import os 
import requests
import pandas as pd
from dotenv import load_dotenv 

def fetch_usda_data(api_key: str, output_path: str):
    
    """
    Fetch cord yield data for Iowa from USDA Quick Stats API
    
    Parameters:
        api_key (str) : API Key to access Quick Stat
        output_path (str): Path to save CSV file 
    """
    
    params = {
        'key' : api_key, 
        'source_desc': 'SURVEY', 
        'sector_desc': 'CROPS',
        'group_desc': 'FIELD CROPS', 
        'commodity_desc': 'CORN', 
        'statisticcat_desc': 'YIELD', 
        'util_practice_desc': 'GRAIN', 
        'agg_level_desc': 'COUNTY', 
        'state_name': 'IOWA', 
        'year__GE': '2016', 
        'year__LE': '2023', 
        'format': 'JSON'
    }
    
    # API endpoit
    url = 'https://quickstats.nass.usda.gov/api/api_GET/'
    
    
    print("Requesting data from USDA Quick Stats API ...")
    
    
    try: 
        response = requests.get(url, params = params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return
    
    print("Data Fetched. Processing...")
    data = response.json().get('data', [])
    
    
    if not data: 
        print("Data not fetched from API. Check parameters and API.")
        
    # Convery from JSON to DataFrame
    df = pd.DataFrame(data)
        
        
    required_columns = ['year', 'state_alpha', 'county_name', 'county_code', 
                        'commodity_desc', 'statisticcat_desc', 'Value', 'unit_desc']
    
    df = df[required_columns]
    
    # Yield value conversion to numeric coerciing error
    df['Value'] = pd.to_numeric(df['Value'], errors = 'coerce')
    
    
    # Remove rows with no yield
    df.dropna(subset=['Value'], inplace = True)
    
    os.makedirs(os.path.dirname(output_path), exist_ok = True )
    df.to_csv(output_path, index = False)
    print(f"Successfuly saved USDA data to {output_path}")


if __name__ == '__main__': 
    
    load_dotenv()
    
    API_KEY = os.getenv('USDA_API_KEY')
    
    if not API_KEY: 
        raise ValueError("USDA_API_KEY not found.")
    
    
    output_file_path = '/data/raw/usda_corn_yield_iowa_2016_2023.csv'
    fetch_usda_data(api_key=API_KEY, output_path = output_file_path)
    