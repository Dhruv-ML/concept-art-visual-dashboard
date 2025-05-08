import pandas as pd
import altair as alt
import streamlit as st
from PIL import Image

# Display logo
logo = Image.open("/Users/dhruvin/Desktop/MC logo.jpg")
st.sidebar.image(logo, width=120)

# Load the dataset
ca = pd.read_csv('/Users/dhruvin/Desktop/My Desktop/Sourcing Analysis/concept art/CAlist.csv', encoding='latin-1')

# Preprocess
ca['Concept Art Experience'] = pd.to_numeric(ca['Concept Art Experience'], errors='coerce')
ca['Total Experience'] = pd.to_numeric(ca['Total Experience'], errors='coerce')
ca['Portfolio'] = ca['Portfolio'].fillna("No portfolio available")
ca['LinkedIn'] = ca['LinkedIn'].fillna("No LinkedIn available")
ca = ca.dropna(subset=['City', 'Studio'])

# Sidebar filters (used to filter both chart and table)
st.sidebar.header("🎛 Filter Talent Pool")
city_sorted = sorted(ca['City'].unique())
studio_sorted = sorted(ca['Studio'].unique())

selected_city = st.sidebar.selectbox("City", ["All"] + city_sorted)
selected_studio = st.sidebar.selectbox("Studio", ["All"] + studio_sorted)
selected_ca_exp = st.sidebar.slider("Minimum Concept Art Experience (Years)", 0, 15, 0)

# Apply filters
filtered_df = ca.copy()
if selected_city != "All":
    filtered_df = filtered_df[filtered_df['City'] == selected_city]
if selected_studio != "All":
    filtered_df = filtered_df[filtered_df['Studio'] == selected_studio]
filtered_df = filtered_df[filtered_df['Concept Art Experience'] >= selected_ca_exp]

# Altair chart (based on filtered_df)
chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x=alt.X('Concept Art Experience:Q',
            title='Concept Art Experience',
            scale=alt.Scale(domain=[0, 15]),
            axis=alt.Axis(tickMinStep=1, format='d')),
    y=alt.Y('Total Experience:Q',
            title='Total Experience',
            scale=alt.Scale(domain=[0, ca['Total Experience'].max() + 2]),
            axis=alt.Axis(tickMinStep=1, format='d')),
    color=alt.Color('Studio:N', legend=None),
    tooltip=[
        'Name', 'Title', 'Studio', 'City',
        'Total Experience', 'Concept Art Experience',
        alt.Tooltip('LinkedIn:N', title='LinkedIn URL'),
        alt.Tooltip('Portfolio:N', title='Portfolio URL')
    ]
).properties(
    width=750,
    height=450,
    title='🎨 Concept Artist Talent Mapping'
).interactive()

# Streamlit layout
st.title("Concept Artist Visual Dashboard")
st.altair_chart(chart, use_container_width=True)

# Data table and CSV download
st.subheader(f"📋 Filtered Results ({len(filtered_df)} profiles)")
if not filtered_df.empty:
    st.dataframe(filtered_df)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data", csv, "filtered_talent.csv", "text/csv")
else:
    st.warning("⚠️ No profiles match the selected filters.")