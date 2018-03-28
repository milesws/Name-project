# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 11:18:34 2018

@author: tannerse
"""

import os
from selenium import webdriver
import requests
import pandas as pd
import re
from time import sleep
import time,datetime

def remove_non_ascii_1(text):
    return ''.join(i for i in text if ord(i)<128)
    
# Read the data.
#df0 = pd.read_stata(r'R:\JoePriceResearch\record_linking\projects\deep_learning\pid_1900census.dta')
df1 = pd.read_stata(r'R:\JoePriceResearch\record_linking\projects\deep_learning\pid_1910census.dta')
#df2 = pd.read_stata(r'R:\JoePriceResearch\record_linking\projects\deep_learning\pid_1920census.dta')

# Drop any duplicates by either ark or pid.
#df0 = df0.drop_duplicates(subset='ark1900', keep=False)
#df0 = df0.drop_duplicates(subset='pid', keep=False)

df1 = df1.drop_duplicates(subset='ark1910', keep=False)
df1 = df1.drop_duplicates(subset='pid', keep=False)

#df2 = df2.drop_duplicates(subset='ark1920', keep=False)
#df2 = df2.drop_duplicates(subset='pid', keep=False)

def Authenticate():
    '''
    Uses the stored credentials from the Family Search object to
    get an API key.
    
    Returns
    -------
    key = API authentication key.
    '''
    #Call chromedriver
    chromedriver = 'R:\\JoePriceResearch\\Python\\chromedriver.exe'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    #with open('Authentication_Key.txt', 'r') as file:
        #key = file.read()
        #make test request here
    

        # Get the webpage.
    driver.get('https://www.familysearch.org')
    #self.driver.find_element_by_css_selector('#global-header > div > div > div.auxilary-links > div > a.sign-in-link.fs-button.fs-button--small.fs-button--minor')
    
    
    # Fill out the form and click submit.
    '''    
    self.driver.find_element_by_id('userName').send_keys(self.username) #######
    self.driver.find_element_by_id('password').send_keys(self.password) ########
    self.driver.find_element_by_xpath('//*[text()="Sign In"]').click()
    '''

    # Click on the authenticate button.
    driver.get('https://www.familysearch.org/platform/')
    driver.find_element_by_xpath('//*[text()="Authenticate"]').click()
    
    driver.find_element_by_id('userName').send_keys("milesws") 
    driver.find_element_by_id('password').send_keys("Cellist1") 
    driver.find_element_by_xpath('//*[text()="Sign In"]').click()
    
    # Wait until the key appears and scrape it.
    key = ''
    while key == '':
        try:
            key = str(driver.find_element_by_xpath('//pre').text).strip()
        except:
            pass
    
    # Return the key.
    driver.quit()
    return key
    
key = Authenticate()

start = time.mktime(datetime.datetime.today().timetuple())
    
# read file get the last id

ids = ''

j = open(r'R:\JoePriceResearch\LIFE-M\Miles Strother\Machine Learning\api_scrape.csv', 'r')
lines = j.readlines()
j.close()
last_id = lines[-1].split(',')[0]

check = False
for z, name in enumerate(df1.pid):
    if name == last_id:
        check = True
        continue
        
    if check == False:
        continue
    
    #print(z, name)
    ids = ids + name + ','
    
    if z%199 == 0 and z != 0:
        #print('enough!')
        ids = ids[:-1]
        
        #ids = 'KWCV-MXB,KWCH-ZSC'
        while True:
            
            pull = requests.get('http://www.familysearch.org/platform/tree/persons?pids=%s' %(ids), 
                                   headers={'Authorization': 'Bearer %s' %(key), 'Accept':'application/json'})
        
            if pull.status_code != 200: 
                sleep(10)
            else:
                break
        
        text = pull.json()
        
        for x in range(len(text['persons'])):
            #print(text['persons'][x]['display']['name'], text['persons'][x]['id'])
            
            id1 = remove_non_ascii_1(text['persons'][x]['display']['name'])
            
            id2 = remove_non_ascii_1(text['persons'][x]['id'])
            
            
            while True:
                
                pull1 = requests.get('http://www.familysearch.org/platform/tree/persons/%s/sources' %(id2), 
                                   headers={'Authorization': 'Bearer %s' %(key), 'Accept':'application/json'})
                if pull1.status_code != 200 and pull1.status_code != 204: 
                    sleep(10)
                else:
                    break
                
            if pull1.status_code == 204:
                continue
            
            text1 = pull1.json()
            
            data = []
            
            if 'sourceDescriptions' in text1.keys():
                    
                for y in range(len(text1['sourceDescriptions'])):
                    #print(text1['sourceDescriptions'][y]['titles'][0]['value'])
                    data.append(remove_non_ascii_1(re.sub(r',',';', text1['sourceDescriptions'][y]['titles'][0]['value'])))
                
                #break ###############
                
            #break   
            # write to a file on the r drive
            j = open(r'R:\JoePriceResearch\LIFE-M\Miles Strother\Machine Learning\api_scrape.csv', 'a')
            j.write(id2 + ',' + id1 + ',' + ','.join(data) + '\n') ##############
            j.close()
            
            end=time.mktime(datetime.datetime.today().timetuple())
            
            if end-start > 7200:
                key = Authenticate()
                start = time.mktime(datetime.datetime.today().timetuple())
            
        #break
        
            ids = ''     
            