# -*- coding: utf-8 -*-
"""
Created on Saturday March 24 at 9:04 am 2018

@author: milesws
"""
import pandas as pd
import numpy as np
from os import listdir
import re

#Establish directory to files of false name matches comparing 1900 to 1910 censuses
files = listdir(r"R:\JoePriceResearch\record_linking\projects\deep_learning\census")
#Convert each file name in directory to string
files_string = " ".join(str(x) for x in files)

#Use regular expression to select 2 files from each state
files1 = re.findall('(?:[a-zA-Z])\w+T2.dta', files_string)

#Create a blank dataframe
df = pd.DataFrame()

#Loop over files selected to clean data to vectorize later
for x in files1:
    directory = r'R:\JoePriceResearch\record_linking\projects\deep_learning\census\\' + x
    
    #Read in each file
    data = pd.read_stata(directory, columns=['gname1900', 'lname1900', 'gname1910', 'lname1910', 'ark1900', 'true'])
    
    #Rename columns      
    data1 = data.rename(index=str, columns={"true": "match", "gname1900":"first_name", "lname1900":"last1", "gname1910":"first2", "lname1910":"last2", "ark1900":"fsid"})
                  
    fn = data1[data1.match == 0]
    
    #Create columns for first, middle and full names
    fn['full1'] = fn.first_name + " " +fn.last1
    fn['full2'] = fn.first_name + " " +fn.last2
    fn['mid1'] = fn.first_name.str.split('\s+').str[1]
    fn['mid2'] = fn.first_name.str.split('\s+').str[1]
    fn['first1'] = fn.first_name.str.split(' ', 1).str[0]
    fn['first2'] = fn.first_name.str.split(' ', 1).str[0]
    
    #Fill in missing values with a space for individals missing a name
    fn = fn.replace(np.NaN, '', regex=True)
    
    #Take a random sample of 10000 per file
    fn1 = fn.sample(n=10000, replace=True)
    
    #Append to a .csv
    fn1.to_csv(r'R:\JoePriceResearch\LIFE-M\Miles Strother\Machine Learning\false_names.csv', mode='a', header=True)
