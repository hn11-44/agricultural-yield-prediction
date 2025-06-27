import pandas as pd
import requests
import os 
import time
from typing import List 



def fetch_nasa_power_data(
    latitude : float, 
    longtitude: float, 
    start_date: str, 
    end_date : str, 
    parameters: List[str]
     
) -> pd.DataFrame: 
    
    """"
    Daily weather from NASA API for specified location and time range. 
    
    """
    
    api_endpoint = "https://power.larc.nasa.gov/api/temporal/daily/point"
    
    
    params = {
        "start": start_date, 
        "end": end_date, 
        "latitude": latitude, 
        "longitude": longtitude, 
        "community": "ag", 
        "parameters": ",".join(parameters), 
        "format": "json", 
        "header": "true"
        }
    
    print("API request --- ")
    print(f"TARGET URL : {api_endpoint}")
    print(f"Request Parameter {params}")
    
    try : 
        response= requests.get(api_endpoint, params = params)
        response.raise_for_status()
        
        data = response.json()
        
        # Data is nested so we need to parse through the paramerter
        df = pd.DataFrame(data['properties']['parameter'])
        
        df['latitude'] = latitude
        df['longitude'] = longtitude
        
        
        # Format the date 
        df['date'] = pd.to_datetime(df.index, format = '%Y%m%d')
        
        return df
    
    except requests.exceptions.RequestException as e: 
        print(f" Error Occured {e}")
        return None 
    
if __name__ == '__main__': 
    
    # Load data with yield and coordinates 
    PROCESSED_DATA_PATH = 'data/processed/iowa_yield_with_coords.csv'
    
    # Where we will be storing our data 
    WEATHER_OUTPUT_DIR = 'data/raw/weather'
    
    # Planting Starts in April
    GROWING_SEASON_START_MONTH = 4
    GROWING_SEASON_START_DAY = 1
    
    # Harvesting Seasons 
    GROWING_SEASON_END_MONTH = 9
    GROWING_SEASON_END_DAY = 30
    
    # Weather variables we require average temperature and total percipitation
    WEATHER_PARAMETERS = ["T2M", "PRECTOTCORR"]

    os.makedirs(WEATHER_OUTPUT_DIR, exist_ok= True)


    df_counties = pd.read_csv(PROCESSED_DATA_PATH)
    
    # Get the counties 
    unique_counties = df_counties.drop_duplicates(subset = ['full_fips_code']).copy()
    
    print(f"Start fetching data for {len(unique_counties)} counties")
    
    
    for index, row in unique_counties.iterrows():
        
        fips = row['full_fips_code']
        lat = row['latitude']
        lon = row['longitude']
        
        
        print(f"\nProcessing county: {row['county_name']} FIPS: {fips}")
        
        for year in range(2016, 2024):
            output_filename = os.path.join(WEATHER_OUTPUT_DIR, f"{year}_{fips}.csv")
            
            
            if os.path.exists(output_filename): 
                print(f"- Year {year}: Already downloaded. Skipping")
            
                continue 
        
            print(f"- Year {year}: Fetching data")
        
        
            start_date = f"{year}{str(GROWING_SEASON_START_MONTH).zfill(2)}{str(GROWING_SEASON_START_DAY).zfill(2)}"
            end_date = f"{year}{str(GROWING_SEASON_END_MONTH).zfill(2)}{str(GROWING_SEASON_END_DAY).zfill(2)}"
        
        
            df_weather = fetch_nasa_power_data(
                latitude=lat, 
                longtitude=lon,
                start_date = start_date, 
                end_date = end_date, 
                parameters=WEATHER_PARAMETERS
            )
        
            if df_weather is not None: 
                df_weather.to_csv(output_filename, index = False)
        
                print(f"Successfuly saved to {output_filename}")
            else: 
                print(f"Failed to get data for year {year}")
            
            time.sleep(1)
    
    print("Weather data fetched and completed ")
    