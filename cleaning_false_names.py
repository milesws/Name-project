# -*- coding: utf-8 -*-
"""
Created on Saturday March 24 at 9:04 am 2018

@author: milesws
"""
import pandas as pd
import numpy as np
from os import listdir
import re

files = listdir(r"R:\JoePriceResearch\record_linking\projects\deep_learning\census")
files_string = " ".join(str(x) for x in files)

files1 = re.findall('(?:[a-zA-Z])\w+T2.dta', files_string)

df = pd.DataFrame()

for x in files1:
    directory = r'R:\JoePriceResearch\record_linking\projects\deep_learning\census\\' + x
    #print(directory)
    data = pd.read_stata(directory, columns=['gname1900', 'lname1900', 'gname1910', 'lname1910', 'ark1900', 'true'])
    print(directory)      
    data1 = data.rename(index=str, columns={"true": "match", "gname1900":"first1", "lname1900":"last1", "gname1910":"first2", "lname1910":"last2", "ark1900":"fsid"})
                  
    fn = data1[data1.match == 0]
    
    fn['full1'] = fn.first1 + " " +fn.last1
    fn['full2'] = fn.first2 + " " +fn.last2
    fn['mid1'] = fn.first1.str.split('\s+').str[1]
    fn['mid2'] = fn.first2.str.split('\s+').str[1]
    
    fn = fn.replace(np.NaN, '', regex=True)
    
    fn1 = fn.sample(n=10000, replace=True)
    
    fn1.to_csv(r'R:\JoePriceResearch\LIFE-M\Miles Strother\Machine Learning\false_names.csv', mode='a', header=True)
