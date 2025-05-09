pip install matplotlib seaborn pandas streamlit
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page layout
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

st.title("🛍️ Retail Analytics Dashboard")

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("retail_data_dirty_large.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.dropna(subset=["purchase_date", "transaction_id", "store_branch"], inplace=True)
    df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter")
selected_stores = st.sidebar.multiselect("Select Store Branch", df["store_branch"].unique(), default=df["store_branch"].unique())
filtered_df = df[df["store_branch"].isin(selected_stores)]

# 1️⃣ Total Sales per Store
st.subheader("1️⃣ Total Sales by Store")
sales_by_store = filtered_df["store_branch"].value_counts()
fig1, ax1 = plt.subplots()
sales_by_store.plot(kind="bar", color="skyblue", ax=ax1)
ax1.set_ylabel("Number of Transactions")
ax1.set_title("Total Transactions per Store")
st.pyplot(fig1)

# 2️⃣ Product Category Distribution
if "product_category" in filtered_df.columns:
    st.subheader("2️⃣ Product Category Distribution")
    fig2, ax2 = plt.subplots()
    filtered_df["product_category"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90, ax=ax2)
    ax2.set_ylabel("")
    ax2.set_title("Product Categories Share")
    st.pyplot(fig2)

# 3️⃣ Sales Trend Over Time
st.subheader("3️⃣ Sales Trend Over Time")
sales_trend = filtered_df.groupby("purchase_date").size()
fig3, ax3 = plt.subplots()
sales_trend.plot(ax=ax3, color="green")
ax3.set_ylabel("Transactions per Day")
ax3.set_title("Sales Trend")
st.pyplot(fig3)

# 4️⃣ Customer Satisfaction vs Discount
if "discount_percentage" in filtered_df.columns and "satisfaction_score" in filtered_df.columns:
    st.subheader("4️⃣ Customer Satisfaction vs Discount")
    fig4, ax4 = plt.subplots()
    sns.scatterplot(data=filtered_df, x="discount_percentage", y="satisfaction_score", hue="payment_method", ax=ax4)
    ax4.set_title("Satisfaction vs Discount")
    st.pyplot(fig4)

# 5️⃣ Top Products Sold
if "product_name" in filtered_df.columns:
    st.subheader("5️⃣ Top Products Sold")
    inventory = filtered_df["product_name"].value_counts().head(10)
    fig5, ax5 = plt.subplots()
    inventory.plot(kind="bar", color="orange", ax=ax5)
    ax5.set_title("Top 10 Products Sold")
    st.pyplot(fig5)

# Footer
st.markdown("---")
st.markdown("✅ Dashboard Completed | © 2025 Retail Analytics")
