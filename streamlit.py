import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import requests

# App Title
st.title("Career Accelerator Program Dashboard - Basic Visualization")

# Dataset URL (GitHub raw URL)
dataset_url = 'https://raw.githubusercontent.com/vaidyamohit/Marketing-Dashboard/main/Dataset%20Marketing.xlsx'

@st.cache
def load_data_from_url(url):
    """Fetch and load Excel sheets as DataFrames from a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        file = BytesIO(response.content)
        customer_info = pd.read_excel(file, sheet_name='Customer Information')  # Update name if incorrect
        return customer_info
    else:
        st.error("Failed to fetch the dataset. Please check the URL.")
        return None

# Load the data
customer_info = load_data_from_url(dataset_url)

if customer_info is not None:
    # Display the dataset
    st.subheader("Dataset Preview")
    st.write(customer_info.head())

    # Basic Graph: Distribution of Ages
    st.subheader("Basic Graph: Age Distribution of Customers")
    fig = px.histogram(customer_info, x='Age', nbins=20, title='Age Distribution of Customers')
    st.plotly_chart(fig)
else:
    st.error("Dataset could not be loaded. Please check the file path or dataset.")
