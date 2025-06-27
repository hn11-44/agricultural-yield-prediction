import streamlit as st
import pandas as pd 
import xgboost as xgb
import numpy as np

# Page conigurations
st.set_page_config(
    page_title = "Iowa Corn Yield Predictor", 
    page_icon = "🌽", 
    layout = 'wide'
)


# Model loading 
@st.cache_resource
def load_model():
    model = xgb.XGBRegressor()
    model.load_model('models/yield_prediction_model.json')
    return model 


model = load_model()




# Application Layout
st.title("🌽 Iowa Corn Yield Predictor")
st.write(
    "This app predicts the corn yield (in bushels per acre) for a county in Iowa based on agricultural and weather data. "
    "Adjust the sliders and input values in the sidebar to see the model's prediction."
)
st.write("---")

# --- Sidebar for User Inputs ---
st.sidebar.header("Input Features")
year = st.sidebar.slider("Year", 2016, 2030, 2024)
latitude = st.sidebar.number_input("Latitude", min_value=40.0, max_value=44.0, value=42.5, step=0.1)
longitude = st.sidebar.number_input("Longitude", min_value=-97.0, max_value=-90.0, value=-93.5, step=0.1)

st.sidebar.subheader("Seasonal Weather Conditions")
T2M_mean = st.sidebar.slider("Seasonal Avg. Temp (°C)", 15.0, 25.0, 20.0)
T2M_max = st.sidebar.slider("Seasonal Max Temp (°C)", 28.0, 40.0, 34.0)
T2M_min = st.sidebar.slider("Seasonal Min Temp (°C)", 0.0, 15.0, 8.0)
T2M_std = st.sidebar.slider("Seasonal Temp Std. Dev.", 5.0, 15.0, 8.5)
PRECTOTCORR_sum = st.sidebar.slider("Total Seasonal Rainfall (mm)", 300.0, 1200.0, 700.0)
PRECTOTCORR_max = st.sidebar.slider("Max Daily Rainfall (mm)", 20.0, 150.0, 60.0)
extreme_heat_days = st.sidebar.slider("Number of Extreme Heat Days (>32°C)", 0, 40, 5)


# We create two columns for the layout
col1, col2 = st.columns([0.6, 0.4]) # 60% width for map, 40% for prediction

with col1:
    # --- NEW SECTION: Map Display ---
    st.subheader("County Location on Map")
    # Create a DataFrame with the selected latitude and longitude for the map
    map_data = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude]
    })
    # Display the map. It will update as the sliders are moved.
    st.map(map_data, zoom=5)
    # ------------------------------

with col2:
    # --- Prediction Logic and Display ---
    st.subheader("Predicted Corn Yield")
    # A button to trigger the prediction
    if st.button("Predict Yield", use_container_width=True):
        # Create a DataFrame from all the user's inputs
        feature_values = {
            'year': [year], 'latitude': [latitude], 'longitude': [longitude],
            'T2M_mean': [T2M_mean], 'T2M_max': [T2M_max], 'T2M_min': [T2M_min],
            'T2M_std': [T2M_std], 'PRECTOTCORR_sum': [PRECTOTCORR_sum],
            'PRECTOTCORR_max': [PRECTOTCORR_max], 'extreme_heat_days': [extreme_heat_days]
        }
        input_df = pd.DataFrame(feature_values)

        # Use the loaded model to make a prediction
        prediction = model.predict(input_df)[0]

        # Display the result using st.metric for a nice visual
        st.metric(label="Bushels per Acre", value=f"{prediction:.2f}")
    else:
        st.info("Click the 'Predict Yield' button to see the result.")

