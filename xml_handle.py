# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 15:44:30 2021

@author: shpri
"""

import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import re

# need to add code number to the products - as a meaning "family" wise

num_pub= [1,2,3,4,5,6,7,8] # XML files devided by the ABC order

final_table = pd.DataFrame()
    
for num in num_pub:
        
    path= rf'C:\Users\shpri\Desktop\scripts\EU\Publication{num}.xml'
    
    tree = ET.parse(path)
    
    root = tree.getroot()
    
    # root.tag
    
    # for child in root:
    #     print(child.tag, child.attrib)
        
    # bleh = [elem.tag for elem in root.iter()]
    
    store= ET.tostring(root, encoding='utf8').decode('utf8')
    
    sample= store[:5000000]
    sample2= store.replace('                ','').replace('\n','')
    
    pests= sample2.split('<Substances>')
        
    pest_dict= {}
    
    pests= pests[1:]
    
#create 4 lists out of the XML- names, product, codes, mrl's with regex:  
    
    for i in range(len(pests)):
        info= []
        names= re.findall('<Name>.*?<',pests[i])
        products= re.findall('<Product_name>.*?<',pests[i]) # a list
        codes=re.findall('<Product_code>.*?<',pests[i]) # a list
        mrls= re.findall('<MRL.*?<',pests[i])   # a list 
        mrls_clean=[]
        for mrl in mrls:  #cleans empty mrl's 
            if mrl!= '<MRL_ft>        <':
                mrls_clean.append(mrl)
        info.append((names[0][6:-1],codes, products, mrls_clean))
        pest_dict[names[0]]= info
        #print(len(mrls_clean),' ',len(products) ) ### make sure lengh fits
        
    
    #pest_dict[names[i]]= list((products,mrls))
        
    
    pest1=list( pest_dict.values())
    
    #name_pest= np.repeat( pest1[0][0], len(pest[1]) )
    
    table= pd.DataFrame()
    
# combine the lists to a dataframe:
    
    for k in list(pest_dict.values()):
        name_pest= np.repeat( k[0][0], len(k[0][1]) )
        rows= pd.DataFrame( np.array( [ name_pest, k[0][1], k[0][2], k[0][3] ] ) .T 
                           ,columns= ['name','code','product','mrl'])
        rows['code']= rows['code'].str[14:-1]
        rows['product']= rows['product'].str[14:-1]
        rows['mrl']= rows['mrl'].str[5:-1]
        table=table.append(rows)
    
    final_table= final_table.append(table)

# combine table for each compound for a full table:  
final_table.to_excel(r'C:\Users\shpri\Desktop\scripts\EU\mrl_table.xlsx')