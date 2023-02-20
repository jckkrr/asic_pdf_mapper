import fitz
import os
import pandas as pd
import plotly.graph_objects as go
from pyvis.network import Network
import pyvis

###########################

def fromPDFtoText(filename):
        
    if filename[-4:] != '.pdf':
        filename += '.pdf' 
        
    doc = fitz.open(filename)
    
    filetext = ""
    for page in doc:
        filetext += page.get_text()
    
    return filetext

##############################

def fromTextToDF(filetext):
    
    df = pd.DataFrame()
    
    lines = filetext.split('\n')

    for n in range(0, len(lines)-1):   ### go through every line
            
            line = lines[n].strip()    
            if ':' in line and ':' == line[-1]:
                key = line.replace(':','').strip()
                    
                value = lines[n+1]
                
                if key in ['Address']:                        
                    if ':' not in lines[n+2] and 'Class' not in lines[n+2]:
                        value = lines[n+1] + lines[n+2]
                      
                ## Now to store the values
                nr = df.shape[0]+1
                df.loc[nr, 'company_name'] = None
                df.loc[nr, 'key'] = key.strip().upper() ## placeholder
                df.loc[nr, 'value'] =  value.replace('  ',' ').strip().upper()                    
                #df.loc[nr, 'file'] = filename.replace('.pdf','')            

    company_name = df.loc[df['key']=='NAME', 'value']
        
    if len(company_name)> 0:
        df['company_name'] = company_name.values[0]
        
    df = df.drop_duplicates().reset_index(drop=True)
    
    return df


###############

def getSingleDoc(filename):

    filetext = fromPDFtoText(filename)
    df = fromTextToDF(filetext)
    df['file'] = filename.split('/')[-1]
    
    return df

################

def plotNetwork(df):
    
    g=Network(width="100%", notebook=True, directed=False) #height=1000, 
    
    for index, row in df.iterrows():
        
        source, target, edge_text = row['company_name'], row['value'], row['key']
        g.add_node(source)
        g.add_node(target)
        g.add_edge(source, target, weight=5, title=edge_text, color='#eaeaea')    
        

    ### Update layout
    
    dfVC = pd.Series(list(df['company_name']) + list(df['value'])).value_counts()
    
    for node in g.nodes:
        
        node['size'] = int(dfVC[node['id']]) ** 1.133
    
        if node['id'] in list(df['company_name']):
            node['color'] = 'rgba(125, 125, 222, 0.4)'
        else:
            node['color'] = 'rgba(0, 150, 100, 0.6)'
            
    pyvis.options.Layout(improvedLayout=True)
    
    #g.show(f'XXX.html')
    
    return g