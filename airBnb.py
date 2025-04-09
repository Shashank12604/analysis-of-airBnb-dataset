import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="🏠 Airbnb NYC Dashboard", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #F9F9F9;
        }
        .block-container {
            padding-top: 2rem;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1a1a1a;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏙️ Airbnb NYC Data Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("AB_NYC_2019.csv")
    df.dropna(subset=['name', 'host_name', 'neighbourhood_group'], inplace=True)
    return df

df = load_data()


st.sidebar.header("🔎 Filters")
area = st.sidebar.multiselect("Select Area", df['neighbourhood_group'].unique(), default=df['neighbourhood_group'].unique())
room_type = st.sidebar.multiselect("Select Room Type", df['room_type'].unique(), default=df['room_type'].unique())
max_price = st.sidebar.slider("Maximum Price", 0, int(df['price'].max()), 500)

filtered_df = df[
    (df['neighbourhood_group'].isin(area)) &
    (df['room_type'].isin(room_type)) &
    (df['price'] <= max_price)
]

col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Listings by Neighbourhood Group")
    fig = px.histogram(filtered_df, x="neighbourhood_group", color="neighbourhood_group")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏠 Room Type Distribution")
    fig, ax = plt.subplots()
    filtered_df['room_type'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"), ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

st.markdown("---")
st.subheader("💲 Price Distribution by Room Type")
fig = px.box(filtered_df, x="room_type", y="price", color="room_type", log_y=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("📆 Availability vs Price")
fig = px.scatter(filtered_df, x="availability_365", y="price", color="neighbourhood_group", size="number_of_reviews", hover_data=["name"])
st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.subheader("👤 Top Hosts by Number of Listings")
top_hosts = filtered_df['host_name'].value_counts().head(10)
fig = px.bar(top_hosts, x=top_hosts.values, y=top_hosts.index, orientation='h', color=top_hosts.values, labels={'x': 'Listings', 'y': 'Host'})
st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.markdown("<center>📈 Dashboard by <b>shashank&ravi</b> ✨ | Dataset: Airbnb NYC</center>", unsafe_allow_html=True)
