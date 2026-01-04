import streamlit as st
try:
    print(st.secrets.keys())
except Exception as e:
    print(f"Error accessing secrets: {e}")
