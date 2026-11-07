# This creates the page for displaying data visualizations.

import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")

# ==========================================
# PART 1: GRAPHS FROM data.json
# ==========================================
st.subheader("Weekly Study Hours by Course")

# Load data from data.json
with open("data.json", "r") as infile:
  myData = json.load(infile)

# Extract the data for the chart
subjects = []
hours = []

for point in myData["data_points"]:
  subjects.append(point["label"])
  hours.append(point["Hours"])

# Static visualization (Bar Chart)
fig, ax = plt.subplots()
ax.bar(subjects, hours)
ax.set_title(myData["chart_title"])
ax.set_xlabel("Course")
ax.set_ylabel("Hours Studied")
st.pyplot(fig)

# PART 1: DYNAMIC VISUALIZATION
st.subheader("Explore Your Study Hours")

# Set up session state
if "selected_course" not in st.session_state:
  st.session_state.selected_course = subjects[0]

if "hours_adjustment" not in st.session_state:
  st.session_state.hours_adjustment = 0

# Let the user choose a course
selected_course = st.selectbox(
    "Choose a course", subjects, key="selected_course"
)

# Find the original hours for the selected course
course_index = subjects.index(selected_course)
original_hours = hours[course_index]

# Let the user adjust the hours
hours_adjustment = st.slider(
    "Adjust study hours", min_value=0, max_value=12, key="hours_adjustment"
)

# Create the dynamic pie chart
adjusted_hours = hours.copy()
adjusted_hours[course_index] = hours_adjustment
dynamic_fig, dynamic_ax = plt.subplots()
dynamic_ax.pie(
    adjusted_hours,
    labels=subjects,
    autopct="%1.1f%%",
    startangle=90,
)
dynamic_ax.set_title(f"Study Hours Distribution - {selected_course}")
st.pyplot(dynamic_fig)

# ==========================================
# PART 2: GRAPHS FROM data.csv
# ==========================================
st.divider()
st.header("Part 2: Visualizations from CSV Data")

# Check if data.csv exists and has data before plotting
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
  # Read the CSV file
  csv_df = pd.read_csv("data.csv", header=None, names=["Category", "Value"])

  # Ensure Value column is numeric for graphing
  csv_df["Value"] = pd.to_numeric(csv_df["Value"], errors="coerce")
  csv_df = csv_df.dropna()

  if csv_df.empty:
    st.warning(
        "No valid numeric data in data.csv yet. Submit some survey responses"
        " first!"
    )
  else:
    # 1. STATIC VISUALIZATION FROM CSV (Bar Chart)
    st.subheader("CSV Static Chart: Values by Category")
    st.bar_chart(csv_df.set_index("Category")["Value"])

    # 2. DYNAMIC VISUALIZATION FROM CSV (Interactive Filter)
    st.subheader("CSV Dynamic Chart: Filtered Data")

    # Session State initialization for dynamic filter
    if "csv_slider_val" not in st.session_state:
      st.session_state.csv_slider_val = float(csv_df["Value"].max())

    max_limit = st.slider(
        "Filter maximum value",
        min_value=0.0,
        max_value=float(csv_df["Value"].max()) + 5.0,
        value=st.session_state.csv_slider_val,
        key="csv_slider",
    )

    # Filter the dataframe based on slider
    filtered_csv_df = csv_df[csv_df["Value"] <= max_limit]

    if filtered_csv_df.empty:
      st.warning("No data matches this filter range.")
    else:
      # Advanced visualization using Matplotlib (st.pyplot)
      fig_csv, ax_csv = plt.subplots()
      ax_csv.bar(
          filtered_csv_df["Category"],
          filtered_csv_df["Value"],
          color="orange",
      )
      ax_csv.set_title("Filtered Values from Survey")
      ax_csv.set_xlabel("Category")
      ax_csv.set_ylabel("Value")

      st.pyplot(fig_csv)
else:
  st.info(
      "The 'data.csv' file is empty or does not exist yet. Fill out the"
      " Survey page to generate data!"
  )
