### streamlit run "C:\Users\Jack\Documents\Python_projects\2023\asic_document_reader\citec_mapper.py"

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

#########################

def convertFiletext(filetext):
    
    df = pd.DataFrame(columns=['source', 'connection', 'target'])
    
    organisation_name = re.findall(r'Current Organisation Details\|Name\|(.+?)\|', filetext)[0]

    def getRe(prewords):

        L = re.findall(prewords + r'\|(.+?)\|', filetext)

        for item in L:
            df.loc[df.shape[0]+1] = item, prewords, organisation_name, 

    getRe('Officer Name')        
    getRe('Address')   
    getRe('Name') 

    df = df.loc[df['source'] != df['target']]
    df = df.drop_duplicates().reset_index(drop=True)

    return df

##################################

def plotNetwork(df):
    
    g=Network(width="100%", notebook=True, directed=False) #height=1000, 
    
    for index, row in df.iterrows():
        
        source, target, edge_text = row['source'], row['target'], row['connection']
        g.add_node(source)
        g.add_node(target)
        g.add_edge(source, target, weight=5, title=edge_text, color='#eaeaea')    
        

    ### Update layout
    
    dfVC = pd.Series(list(df['source']) + list(df['target'])).value_counts()
    
    for node in g.nodes:
        
        node['size'] = int(dfVC[node['id']]) ** 1.133
    
        if node['id'] in list(df['source']):
            node['color'] = 'rgba(125, 125, 222, 0.4)'
        else:
            node['color'] = 'rgba(0, 150, 100, 0.6)'
            
        node['font'] = str(7 + int(dfVC[node['id']]) ** 0.75) + ' manrope #181818'
        
            
    pyvis.options.Layout(improvedLayout=True)
    
    #g.show(f'XXX.html')
    
    return g

####################################

st.write('Constituent Investigative Analytics')

st.write('# ASIC MAPPER #####')

st.write('Fed in your ASIC Business Registry PDFs. It will return an interactive network map.') 

#########################

df = pd.DataFrame()

uploaded_files = st.file_uploader("", accept_multiple_files=True)

for filename in uploaded_files:
        
    with fitz.open(stream=filename.read(), filetype="pdf") as doc:    
        filetext = ""
        for page in doc:            
            filetext += page.get_text()
          
    filetext = filetext.replace('\n','|')
    #st.write(filetext)
        
    dfx = convertFiletext(filetext)
    dfx['file'] = filename.name
    
    df = pd.concat([df, dfx])
    df = df.reset_index(drop=True)
    
#######

if df.shape[0] > 0:
        
    st.dataframe(df, height=250)
    
    #### Get network
    
    G = plotNetwork(df)

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