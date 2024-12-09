import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# App Title
st.title("Career Accelerator Program Dashboard")

# Dataset URL (GitHub raw URL)
dataset_url = 'https://raw.githubusercontent.com/vaidyamohit/Marketing-Dashboard/main/Dataset%20Marketing.xlsx'

@st.cache
def load_data_from_url(url):
    """Fetch and load Excel sheets as DataFrames from a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        file = BytesIO(response.content)
        customer_info = pd.read_excel(file, sheet_name='Customer Information')
        competitor_info = pd.read_excel(file, sheet_name='Competitor Information')
        marketing_data = pd.read_excel(file, sheet_name='Marketing Data')
        survey_data = pd.read_excel(file, sheet_name='Survey Data')
        enrollment_data = pd.read_excel(file, sheet_name='Enrollment and Revenue Metrics')
        return customer_info, competitor_info, marketing_data, survey_data, enrollment_data
    else:
        st.error("Failed to fetch the dataset. Please check the URL.")
        return None, None, None, None, None

# Load the data
customer_info, competitor_info, marketing_data, survey_data, enrollment_data = load_data_from_url(dataset_url)

if customer_info is not None:
    # Sidebar Filters
    st.sidebar.header("Filters")
    age_filter = st.sidebar.slider("Age Range", int(customer_info['Age'].min()), int(customer_info['Age'].max()), (25, 40))
    gender_filter = st.sidebar.multiselect("Gender", customer_info['Gender'].unique(), default=customer_info['Gender'].unique())
    education_filter = st.sidebar.multiselect("Education Level", customer_info['Education Level'].unique())
    industry_filter = st.sidebar.multiselect("Industry", customer_info['Industry'].unique())

    # Apply Filters
    filtered_data = customer_info[
        (customer_info['Age'] >= age_filter[0]) &
        (customer_info['Age'] <= age_filter[1]) &
        (customer_info['Gender'].isin(gender_filter)) &
        (customer_info['Education Level'].isin(education_filter if education_filter else customer_info['Education Level'])) &
        (customer_info['Industry'].isin(industry_filter if industry_filter else customer_info['Industry']))
    ]

    # Display Filtered Data
    st.subheader("Filtered Customer Data")
    st.write(filtered_data)

    # Competitor Analysis
    st.subheader("Competitor Pricing Insights")
    competitor_chart = competitor_info.groupby('Competitor Name').agg({'Course Price': 'mean', 'Enrollment Numbers': 'sum'})
    st.bar_chart(competitor_chart)

    # Marketing Campaign Performance
    st.subheader("Marketing Campaign Performance")
    marketing_summary = marketing_data.groupby('Campaign Type').agg({'Ad Spend': 'sum', 'CTR': 'mean', 'Conversion Rate': 'mean'})
    st.line_chart(marketing_summary[['Ad Spend', 'CTR', 'Conversion Rate']])

    # Survey Insights
    st.subheader("Survey Insights")
    feature_importance = survey_data[['Feature Importance (Mentorship)', 'Feature Importance (Projects)', 'Feature Importance (Job Assistance)']].mean()
    st.write(feature_importance)
    st.bar_chart(feature_importance)

    # Enrollment and Revenue
    st.subheader("Enrollment and Revenue Insights")
    enrollment_summary = enrollment_data.groupby('Enrollment Date').agg({'Revenue Per Customer': 'sum', 'Cost Per Acquisition (CPA)': 'mean'})
    st.area_chart(enrollment_summary)

    # KPIs
    st.sidebar.header("Key Metrics")
    total_revenue = enrollment_data['Revenue Per Customer'].sum()
    avg_cpa = enrollment_data['Cost Per Acquisition (CPA)'].mean()
    roi = enrollment_data['ROI by Channel'].mean()

    st.sidebar.metric("Total Revenue", f"${total_revenue:,.2f}")
    st.sidebar.metric("Average CPA", f"${avg_cpa:,.2f}")
    st.sidebar.metric("Average ROI", f"{roi:.2%}")
else:
    st.info("Dataset not loaded. Please check the URL or dataset format.")
