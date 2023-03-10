### streamlit run "C:\Users\Jack\Documents\Python_projects\2023\asic_document_reader\streamlit_file.py"

from bs4 import BeautifulSoup
import fitz
import pandas as pd
import plotly.graph_objects as go
from pyvis.network import Network
import pyvis
import re
import streamlit as st
import streamlit.components.v1 as components
import time

import projectTools

######


st.write('Constituent Investigative Analytics')

st.write('# ASIC MAPPER #####')

st.write('Fed in your ASIC Business Registry PDFs. It will return an interactive network map.') 

#########################

df = pd.DataFrame()

uploaded_files = st.file_uploader("", accept_multiple_files=True)

for filename in uploaded_files:
    
    #st.write(filename)
    
    with fitz.open(stream=filename.read(), filetype="pdf") as doc:    
        filetext = ""
        for page in doc:            
            filetext += page.get_text()
            
        #st.write(filetext)
        
    dfx = projectTools.fromTextToDF(filetext)
    dfx['file'] = filename.name
    
    df = pd.concat([df, dfx])
    df = df.reset_index(drop=True)
    
if df.shape[0] > 0:
    
    keys = df['key'].unique()
    initial_selections = ['NAME', 'ACN'] + [x for x in keys if 'ADDRESS' in x]
    initial_selections = [x for x in initial_selections if x in keys]
    
    selected_keys = st.multiselect(
        'Which key types you would like to include:',
        keys,
        initial_selections)  
    
    df = df.loc[df['key'].isin(selected_keys)]
    df = df.loc[df['company_name'] != df['value']]
    
    
    ### Because names can appear in various guises, here they can be updated
    node_labels =  sorted(df['value'].unique())
    
    selected_labels = st.multiselect(
        'Select a node you would like to update',
        node_labels
    )
    
    updated_labels = st.text_input('Change names to (Please seperate by comma)', '')
    updated_labels = updated_labels.split(',')
    
    for selected_label in selected_labels:
        
        n = selected_labels.index(selected_label)
        
        updated_label = selected_label
        if len(selected_labels) == len(updated_labels):
            updated_label = updated_labels[n].strip()
                    
        df.loc[df['value'] == selected_label, 'value'] = updated_label
    
    ###
    
    st.dataframe(df, height=250)
    
    #### Get network
    
    G = projectTools.plotNetwork(df)

    ### Display network
    path = '/tmp'
    G.save_graph(f'temp.html')
    
    HtmlFile = open(f'temp.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=550)
    
    downloadHTML = str(open(f'temp.html', 'r', encoding='utf-8').read())
    

    ### when running deployed version, this is necessary as it puts a container around the network that affects bespoke layout updates
    soup = BeautifulSoup(downloadHTML, 'html.parser')
    div_card = soup.find('div', {'class': 'card'})  
    div_mynetwork = soup.find('div', {'id': 'mynetwork'}) 
    downloadHTML = str(soup).replace(str(div_card), str(div_mynetwork))

    downloadHTML = downloadHTML.replace('border: 1px', 'border: 0px').replace('height: 600px;', 'height: 100%')
    downloadHTML = downloadHTML.replace('</head>', '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;900&display=swap"></head>')  ### add font
    
    saved_filename = 'asic_network_map_' + time.strftime("%Y%m%d%H%M%S")

    st.download_button(
        "Press to Download HTML",
        downloadHTML,
        f"{saved_filename}.html"
    )
    
####### 
st.write('')
st.write('')
st.write('&#11041; More tools at www.constituent.au')
    
    

        
   
    
    
    


        
        
       