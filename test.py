import fitz

import streamlit as st
uploaded_files = st.file_uploader("", accept_multiple_files=True)

for filename in uploaded_files:
    
    st.write(filename)