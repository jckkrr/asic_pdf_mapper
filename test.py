import fitz

import streamlit as st

#############


#uploaded_files = st.file_uploader("", accept_multiple_files=True)

uploaded_files = ['http://constituent.au/2d3432373339313234383.pdf']

for uploaded_file in uploaded_files:
    
    st.write(uploaded_file)

    st.write("Filename: ", uploaded_file.name)
        
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:       
            
        st.write(doc)
        
        for page in doc:      
            
            newtext = page.getText()
            
            st.write(newtext)
            
    
    
    