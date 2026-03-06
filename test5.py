import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("free_time_gaps_nodewise.csv")

df['gap_start'] = pd.to_datetime(df['gap_start'])
df['gap_end'] = pd.to_datetime(df['gap_end'])
df['date'] = pd.to_datetime(df['date'])

# -------------------------
# Title
# -------------------------
st.title("Telescope Gap Timeline Dashboard")

# -------------------------
# Node Selection
# -------------------------
nodes = df['node_id'].unique()

selected_node = st.selectbox(
    "Select Node",
    nodes
)

# Filter node
node_df = df[df["node_id"] == selected_node]

# -------------------------
# Date Selection
# -------------------------
dates = node_df['date'].dt.date.unique()

selected_date = st.selectbox(
    "Select Date",
    dates
)

# Filter date
filtered_df = node_df[node_df['date'].dt.date == selected_date]

# -------------------------
# Plot Gantt Chart
# -------------------------
fig = px.timeline(
    filtered_df,
    x_start="gap_start",
    x_end="gap_end",
    y="node_id",
    color="gap_minutes",
    hover_data=[
        "gap_start",
        "gap_end",
        "gap_minutes",
        "gap_duration"
    ],
    title=f"Gaps | Node: {selected_node} | Date: {selected_date}"
)

fig.update_yaxes(autorange="reversed")

fig.update_layout(
    xaxis=dict(
        tickformat="%H:%M",
        title="Time"
    ),
    height=500
)

st.plotly_chart(fig, use_container_width=True)