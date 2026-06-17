import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("customer_segments.csv")
summary = pd.read_csv("segment_summary.csv")
pca_df = pd.read_csv("pca_data.csv")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Overview",
        "Segment Analysis",
        "PCA Visualization",
        "Top Customers"
    ]
)
st.info(
    """
    This project segments customers using
    RFM Analysis (Recency, Frequency, Monetary)
    and K-Means Clustering.

    The objective is to identify valuable,
    loyal, active, and at-risk customers
    for targeted marketing strategies.
    """
)
# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------

if page == "Overview":

    st.title("🛒 Customer Segmentation Dashboard")
    st.markdown("### RFM Analysis + K-Means Clustering")

    total_customers = len(df)
    total_revenue = df['Monetary'].sum()
    avg_revenue = df['Monetary'].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

    with col2:
        st.metric(
            "Total Revenue",
            f"{total_revenue:,.0f}"
        )

    with col3:
        st.metric(
            "Average Revenue",
            f"{avg_revenue:,.0f}"
        )

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

# --------------------------------------------------
# SEGMENT ANALYSIS PAGE
# --------------------------------------------------

elif page == "Segment Analysis":

    st.title("📈 Segment Analysis")

    st.subheader("Customer Segment Distribution")

    fig1, ax1 = plt.subplots(figsize=(8, 5))

    df['Segment'].value_counts().plot(
        kind='bar',
        ax=ax1
    )

    ax1.set_xlabel("Segment")
    ax1.set_ylabel("Number of Customers")
    ax1.set_title("Customer Distribution")

    st.pyplot(fig1)

    st.divider()

    st.subheader("Revenue Contribution by Segment")

    segment_revenue = df.groupby(
        'Segment'
    )['Monetary'].sum()

    fig2, ax2 = plt.subplots(figsize=(7, 7))

    segment_revenue.plot(
        kind='pie',
        autopct='%1.1f%%',
        ax=ax2
    )

    ax2.set_ylabel("")

    st.pyplot(fig2)

    st.divider()

    st.subheader("Segment Summary")

    st.dataframe(
        summary,
        use_container_width=True
    )
# --------------------------------------------------
# PCA VISUALIZATION
# --------------------------------------------------

elif page == "PCA Visualization":

    st.title("🔍 PCA Cluster Visualization")

    st.write(
        """
        PCA (Principal Component Analysis) reduces
        customer data into two dimensions so that
        customer segments can be visualized.
        """
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(
        pca_df["PCA1"],
        pca_df["PCA2"],
        c=pca_df["Cluster"]
    )

    ax.set_title(
        "Customer Segments using PCA"
    )

    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")

    plt.colorbar(
        scatter,
        label="Cluster"
    )

    st.pyplot(fig)

    st.subheader("PCA Dataset Preview")

    st.dataframe(
        pca_df.head(),
        use_container_width=True
    )
# --------------------------------------------------
# TOP CUSTOMERS PAGE
# --------------------------------------------------

elif page == "Top Customers":

    st.title("🏆 Top Customers")

    top_customers = df.sort_values(
        by="Monetary",
        ascending=False
    ).head(10)

    st.subheader("Top 10 Customers by Spending")

    st.dataframe(
        top_customers,
        use_container_width=True
    )

    st.divider()

    st.subheader("Search Customer")

    customer_id = st.number_input(
        "Enter Customer ID",
        min_value=0.0
    )

    result = df[
        df["CustomerID"] == customer_id
    ]

    if len(result) > 0:

        st.success("Customer Found")

        st.dataframe(
            result,
            use_container_width=True
        )

    else:

        st.info(
            "Enter a valid Customer ID"
        )