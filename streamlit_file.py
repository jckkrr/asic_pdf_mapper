### streamlit run "C:\Users\Jack\Documents\Python_projects\2023\asic_document_reader\streamlit_file.py"

import fitz
import pandas as pd
import plotly.graph_objects as go
from pyvis.network import Network
import pyvis
import re
import streamlit as st
import streamlit.components.v1 as components

import projectTools

######

st.write('#### CONSTITUENT INVESTIGATIVE ANALYTICS ####')

#########################

df = pd.DataFrame()

uploaded_files = st.file_uploader("", accept_multiple_files=True)

for filename in uploaded_files:
    
    st.write(filename)
    
    with fitz.open(stream=filename.read(), filetype="pdf") as doc:
        
        doc = fitz.open(filename)
        st.write(doc)
        
        filetext = ""
        for page in doc:            
            newtext = page.getText()
            filetext += newtext
        #st.write(filetext)
        
    dfx = projectTools.fromTextToDF(filetext)
    dfx['file'] = re.findall('\'.*\.pdf', str(filename))[0][1:]
    
    df = pd.concat([df, dfx])
    df = df.reset_index(drop=True)
    
if df.shape[0] > 0:
    
    keys = df['key'].unique()
    initial_selections = ['NAME', 'ACN'] + [x for x in keys if 'ADDRESS' in x]
    initial_selections = [x for x in initial_selections if x in keys]
    
    selected_keys = st.multiselect(
        'Which row types (keys) to include:',
        keys,
        initial_selections)  
    
    df = df.loc[df['key'].isin(selected_keys)]
    df = df.loc[df['company_name'] != df['value']]
    
    st.dataframe(df)
        
    G = projectTools.plotNetwork(df)
    
    ### display
    path = '/tmp'
    G.save_graph(f'temp.html')
    
    HtmlFile = open(f'temp.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=500)
    
    downloadHTML = str(open(f'temp.html', 'r', encoding='utf-8').read()).replace('border: 1px', 'border: 0px').replace('height: 500px;', 'height: 100%')
    st.download_button(
        "Press to Download HTML",
        downloadHTML,
        "test.html"
    )
    
    
    
    
    

        
   
    
    
    


        
        
       