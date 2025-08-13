import streamlit as st
import floor_plan_visualizer
import productivity_reporter  # assuming you have this

st.sidebar.title("ConstructAI Dashboard")
page = st.sidebar.radio("Select a tool", ["Floor Plan Visualizer", "Productivity Reporter"])

if page == "Floor Plan Visualizer":
    floor_plan_visualizer.app()
elif page == "Productivity Reporter":
    productivity_reporter.app()
