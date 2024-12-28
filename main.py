import streamlit as st
import pandas as pd
import json
import glob
import os

# Function to load JSON data
def load_json(file):
    return json.load(file)

# Function to load CSV data
def load_csv(file):
    return pd.read_csv(file)

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Preloaded Data", "Upload New Data"])

# Initialize data list
data = []

# Folder path for preloaded data
folder_path = "C:/Users/Shyam/OneDrive/Desktop/Projects/StreamLit-WebApp/aws_data"

# Load files from the folder if on "Preloaded Data" page
if page == "Preloaded Data":
    file_paths = glob.glob(f"{folder_path}/*")
    for file_path in file_paths:
        try:
            if file_path.endswith(".json"):
                with open(file_path, "r") as file:
                    file_data = json.load(file)
                    data.append(file_data)
            elif file_path.endswith(".csv"):
                csv_data = pd.read_csv(file_path)
                data.extend(csv_data.to_dict(orient="records"))
        except Exception as e:
            st.write(f"Could not load file {file_path}: {e}")

    if data:
        df = pd.DataFrame(data)
        st.write("### Data Overview")
        st.write(df.describe())

        if "Duration" in df.columns and "Accuracy" in df.columns:
            st.write("### Duration and Accuracy Over Time")
            st.line_chart(df[["Duration", "Accuracy"]])

        jerk_columns = [col for col in df.columns if "Jerk Score" in col]
        if jerk_columns:
            st.write("### Jerk Scores")
            jerk_scores = df[jerk_columns]
            st.bar_chart(jerk_scores)

        if "latitude" in df.columns and "longitude" in df.columns:
            map_data = df[["latitude", "longitude"]].dropna()
            st.write("### Location Data")
            st.map(map_data)

        if "Hand" in df.columns:
            hand_choice = st.sidebar.selectbox("Filter by Hand", df["Hand"].unique())
            filtered_df = df[df["Hand"] == hand_choice]
            st.write(f"Filtered data for {hand_choice} hand:", filtered_df)
    else:
        st.write("No preloaded data found. Please check the files and folder path.")

# Page for uploading new data
elif page == "Upload New Data":
    uploaded_file = st.file_uploader("Upload a CSV or JSON file", type=["csv", "json"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".json"):
                file_data = load_json(uploaded_file)
                data.append(file_data)
            elif uploaded_file.name.endswith(".csv"):
                csv_data = load_csv(uploaded_file)
                data.extend(csv_data.to_dict(orient="records"))

            if data:
                df = pd.DataFrame(data)
                st.write("### Uploaded Data Overview")
                st.write(df.describe())

                if "Duration" in df.columns and "Accuracy" in df.columns:
                    st.write("### Duration and Accuracy Over Time")
                    st.line_chart(df[["Duration", "Accuracy"]])

                jerk_columns = [col for col in df.columns if "Jerk Score" in col]
                if jerk_columns:
                    st.write("### Jerk Scores")
                    jerk_scores = df[jerk_columns]
                    st.bar_chart(jerk_scores)

                if "latitude" in df.columns and "longitude" in df.columns:
                    map_data = df[["latitude", "longitude"]].dropna()
                    st.write("### Location Data")
                    st.map(map_data)

                if "Hand" in df.columns:
                    hand_choice = st.sidebar.selectbox("Filter by Hand", df["Hand"].unique())
                    filtered_df = df[df["Hand"] == hand_choice]
                    st.write(f"Filtered data for {hand_choice} hand:", filtered_df)
        except Exception as e:
            st.write(f"Could not load uploaded file: {e}")
    else:
        st.write("Please upload a file to display the data.")
