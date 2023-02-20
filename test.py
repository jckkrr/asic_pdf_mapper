### streamlit run "C:\Users\Jack\Documents\Python_projects\2023\asic_document_reader\test.py"

import fitz
import streamlit as st

#############

uploaded_file = st.file_uploader("")

st.write(uploaded_file)



if uploaded_file != None:
    
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    

    
    st.write(doc.page_count)
    st.write(doc.name, len(doc.name))
    
    for page in doc:
        
        t = page.get_text()
    
        st.write(t)
    
    