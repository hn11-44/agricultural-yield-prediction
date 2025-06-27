# 🌽 Multi-Modal Agricultural Yield Prediction

![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

This project is an end-to-end machine learning application that predicts corn yield (in bushels per acre) for counties in Iowa. It leverages a multi-modal approach, combining historical agricultural data with daily weather data to train a predictive XGBoost model. The final model is deployed as an interactive web application using Streamlit.

**[➡️ View the Live Streamlit App Here!]([https://iowa-corn-prediction.streamlit.app])**

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technical Stack](#-technical-stack)
- [Project Structure](#-project-structure)
- [Setup and Installation](#-setup-and-installation)
- [Usage](#-usage)
- [Model Performance](#-model-performance)
- [Future Work](#-future-work)
- [License](#-license)
- [Contact](#-contact)

---

## 📖 Project Overview

The goal of this project was to build a complete, end-to-end data science application, from initial brainstorming and complex data acquisition to a final, deployed machine learning model. The model predicts corn yield, a critical metric for economic and agricultural planning, by learning patterns from various data sources. The process involved extensive data wrangling, robust environment setup using Conda, feature engineering, model training, and deployment.

## ✨ Key Features

- **Multi-Modal Data Ingestion:** Programmatically fetches data from multiple sources, including the USDA Quick Stats API for yield data and the NASA POWER API for daily weather data.
- **Data Enrichment:** Combines datasets by enriching yield data with geographic coordinates based on county FIPS codes.
- **Feature Engineering:** Transforms raw daily weather data (temperature, precipitation) into meaningful seasonal features like averages, sums, and counts of extreme weather days.
- **Machine Learning Model:** Utilizes an XGBoost Regressor model, a powerful gradient boosting algorithm, to predict crop yield.
- **Interactive Web Application:** The final model is deployed using Streamlit, providing an easy-to-use interface with sliders and inputs for real-time predictions.

## 🛠️ Technical Stack

- **Language:** Python 3.11
- **Environment Management:** Conda
- **Core Libraries:** Pandas, NumPy, Scikit-learn
- **Machine Learning:** XGBoost
- **Web App:** Streamlit
- **Data Sources:** USDA NASS API, NASA POWER API

## 📁 Project Structure


agricultural-yield-prediction/
├── app.py                      # Main script for the Streamlit application
├── data/
│   ├── raw/                    # Raw, immutable data downloaded from sources
│   └── processed/              # Cleaned and processed data ready for modeling
├── models/                     # Saved/serialized production model
├── notebooks/                  # Jupyter notebooks for exploration, cleaning, and modeling
├── src/
│   └── data_ingestion/         # Scripts for programmatically downloading data
├── environment.yml             # Conda environment file for reproducibility
└── README.md                   # This file

## ⚙️ Setup and Installation

To set up this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hn11-44/agricultural-yield-prediction
    cd agricultural-yield-prediction
    ```

2.  **Create and activate the Conda environment:** Make sure you have Anaconda or Miniconda installed. This command will create a new environment named `ml-project-env` using the provided file.
    ```bash
    conda env create -f environment.yml
    conda activate ml-project-env
    ```

3.  **(Note on Data):** The project includes scripts to download data. However, due to potential network issues with the NASA API, a pre-compiled weather dataset is required for full functionality. A sample can be provided upon request.

## 🚀 Usage

Once the environment is set up, you can run the interactive web application:

1.  **Navigate to the project root directory** in your terminal.
2.  **Ensure the conda environment is active.**
3.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
This will launch the application in your web browser. You can also explore the Jupyter notebooks in the `notebooks/` directory to see the step-by-step process of data cleaning, feature engineering, and model training.

## 📊 Model Performance

The baseline XGBoost model was trained on 8 years of data (2016-2023) for 99 Iowa counties. The performance on the unseen test set is as follows:

- **R-squared (R²):** **0.666** (The model explains ~67% of the variance in crop yield.)
- **Mean Absolute Error (MAE):** **8.01 Bushels/Acre** (On average, the model's prediction is off by ~8 bushels/acre.)
