### streamlit run "C:\Users\Jack\Documents\Python_projects\2023\asic_document_reader\test.py"

import fitz
import streamlit as st

#############

uploaded_file = st.file_uploader("")

st.write(uploaded_file)

if uploaded_file != None:
    
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:    
        
        st.write(doc.page_count)
        
        filetext = ""
        for page in doc: 
            
            st.write(page)
            
            newtext = page.getText()
            filetext += newtext
            
        st.write(filetext)
    