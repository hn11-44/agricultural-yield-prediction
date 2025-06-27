import pandas as pd
import os 


def fetch_coords(url : str, output_path: str):
    
    """
    Data enrichments stage, where we get the US country coordinate 
    data and save it as a CSV. This will sever as our lookup table. 
    Downloading the pre-processed country coordinates and saving it. 
    Parameters:
        url (str): URL for our raw CSV data 
        output_path (str): Path to save output file. 

    """
    
    print(f"Fetching country coordinates from {url}")
    
    
    try: 
        df = pd.read_csv(url, sep = '\t', dtype= {'GEOID': str}, encoding = 'latin-1' )
    except Exception as e: 
        print("Failed to fetch CSV file : {e}")
        
    df.columns = df.columns.str.strip()
    
    print("Data fecthed succssefully. Processing...")
    
    # We will joing our FIPS code from our USDA data ('county_code)
    
    required_cols = {
        'GEOID': 'county_code',
        'INTPTLAT' : 'latitude', 
        'INTPTLONG': 'longitude'
    }
    
    if not all(col in df.columns for col in required_cols.keys()):
        print(f"Error : Downloaded file does not contain the expected columns {list(required_cols.keys())}")
        print(f"Available columns are : {df.columns.tolist()}")
        
    df_coords = df[list(required_cols.keys())].copy()
    df_coords.rename(columns=required_cols, inplace = True)
    
    
    df_coords['county_code'] = pd.to_numeric(df_coords['county_code'], errors = 'coerce')
    df_coords.dropna(inplace=True)
    df_coords['county_code'] = df_coords['county_code'].astype(int)
        
    # Save the File
    os.makedirs(os.path.dirname(output_path), exist_ok = True)
    df_coords.to_csv(output_path, index= False)
    print(f"Successfully saved cleaned coordinates data to {output_path}")
    
    
    
if __name__ == '__main__':
    
    COORDS_URL = 'https://raw.githubusercontent.com/josh-byster/fips_lat_long/refs/heads/master/counties.txt'
    output_file_path = 'data/raw/county_coordinates.csv'
    
    fetch_coords(COORDS_URL, output_file_path)