import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Attrition Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("BankChurners.csv")
    df['Age_Group'] = pd.cut(df['Customer_Age'],
        bins=[25,35,45,55,65,75],
        labels=['25-35','35-45','45-55','55-65','65+'])
    return df

df = load_data()

# Title
st.title("Customer Attrition Dashboard")
st.markdown("---")

# Sidebar Filters
st.sidebar.header("Filters")
age_min, age_max = st.sidebar.slider("Age Range", 25, 75, (25, 75))
income_options = ["All"] + list(df['Income_Category'].unique())
income = st.sidebar.selectbox("Income Category", income_options)

# Apply filters
filtered = df[(df['Customer_Age'] >= age_min) & (df['Customer_Age'] <= age_max)]
if income != "All":
    filtered = filtered[filtered['Income_Category'] == income]

# KPIs
total = len(filtered)
churned = len(filtered[filtered['Attrition_Flag'] == 'Attrited Customer'])
retained = total - churned
rate = round(churned / total * 100, 1) if total else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total:,}")
col2.metric("Churned", f"{churned:,}")
col3.metric("Retained", f"{retained:,}")
col4.metric("Attrition Rate", f"{rate}%")

st.markdown("---")

# Charts row
c1, c2 = st.columns(2)

with c1:
    st.subheader("Countplot — Customers by Age Group")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(x='Age_Group', hue='Attrition_Flag', data=filtered, ax=ax,
                  palette={'Attrited Customer':'#A32D2D','Existing Customer':'#3B6D11'})
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Count")
    ax.legend(title="Status", labels=["Attrited", "Existing"])
    st.pyplot(fig)

with c2:
    st.subheader("Boxplot — Age Distribution")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.boxplot(x='Attrition_Flag', y='Customer_Age', data=filtered, ax=ax2,
                palette={'Attrited Customer':'#A32D2D','Existing Customer':'#3B6D11'})
    ax2.set_xlabel("Status")
    ax2.set_ylabel("Age")
    st.pyplot(fig2)

c3, c4 = st.columns(2)

with c3:
    st.subheader("Attrition Rate by Income")
    inc_group = df.groupby('Income_Category')['Attrition_Flag'].apply(
        lambda x: (x == 'Attrited Customer').sum() / len(x) * 100).reset_index()
    inc_group.columns = ['Income', 'Attrition Rate %']
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.barplot(x='Attrition Rate %', y='Income', data=inc_group, color='#185FA5', ax=ax3)
    st.pyplot(fig3)

with c4:
    st.subheader("Attrition Rate by Age Group")
    age_group = filtered.groupby('Age_Group')['Attrition_Flag'].apply(
        lambda x: (x == 'Attrited Customer').sum() / len(x) * 100).reset_index()
    age_group.columns = ['Age Group', 'Attrition Rate %']
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.barplot(x='Age Group', y='Attrition Rate %', data=age_group, color='#A32D2D', ax=ax4)
    st.pyplot(fig4)