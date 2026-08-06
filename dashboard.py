import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components # <--- NEW IMPORT for reading HTML files

# ---------------------------------------------------------
# 1. PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NYC Housing & Tacos")

st.title("The Taco Bell Real Estate Index")
st.markdown("""
**Objective:** Analyzing whether access to fast food (Taco Bell vs. Chipotle) correlates 
with housing prices in New York City. 
""")

# ---------------------------------------------------------
# 2. LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    # Update path if needed
    df = pd.read_csv('/Users/aidantyler/Desktop/Datathon2026/The-Lego-Batman-2-Enjoyers-Datathon-2026-Sponsored-by-Databricks/nyc_housing_with_distances.csv')
    #df = df[(df['sale_price'] > 10000) & (df['sale_price'] < 5000000)]
    df = df[df['bldgarea'] > 100]
    return df

try:
    df = load_data()
except:
    st.error("Could not find the CSV file! Check the path.")
    st.stop()

# ---------------------------------------------------------
# 3. SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("Filter Options")
borough = st.sidebar.selectbox("Select Borough", ["All"] + list(df['borough_y'].unique()))

if borough != "All":
    filtered_df = df[df['borough_y'] == borough]
else:
    filtered_df = df

# ---------------------------------------------------------
# 4. METRICS
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Avg Home Price", f"${filtered_df['sale_price'].mean():,.0f}")
col2.metric("Avg Dist to Taco Bell", f"{filtered_df['dist_to_tacobell'].mean():.2f} miles")
col3.metric("Avg Dist to Chipotle", f"{filtered_df['dist_to_chipotle'].mean():.2f} miles")

# ---------------------------------------------------------
# 5. CHARTS & MAP
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📉 Price vs. Distance", "🗺️ Interactive Map"])

with tab1:
    st.subheader(f"Does Proximity Matter in {borough}?")
    fig = px.scatter(
        filtered_df, 
        x="dist_to_tacobell", 
        y="sale_price", 
        color="borough_y", 
        trendline="ols", 
        title="Price vs. Distance to Taco Bell",
        opacity=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Full NYC Map (Boroughs & Clusters)")
    
    # --- NEW CODE STARTS HERE ---
    # This reads the HTML file you created in the previous step
    map_path = "nyc_borough_map_final.html" 
    
    try:
        with open(map_path, 'r') as f:
            map_html = f.read()
            
        # This renders the HTML file inside the dashboard
        # height=600 gives it plenty of space
        components.html(map_html, height=700, scrolling=False)
        
        
    except FileNotFoundError:
        st.error(f"Could not find '{map_path}'. Make sure you ran the map generation script!")