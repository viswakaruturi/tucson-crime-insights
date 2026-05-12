import pandas as pd
import streamlit as st

DATA_PATH = "data/processed/tpd_2018_2025.csv"

def clean_crime(label):
    if " - " in label:
        return label.split(" - ", 1)[1].title()
    return label.title()

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, low_memory=False)
    df["CrimeLabel"] = df["UCRDescription"].apply(clean_crime)
    return df