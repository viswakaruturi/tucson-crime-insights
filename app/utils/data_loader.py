import pandas as pd
import streamlit as st
 
PATH = "data/processed/tpd_2018_2025.csv"
 
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(PATH, low_memory = False)
    return df