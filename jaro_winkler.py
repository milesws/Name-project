# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:29:35 2018

@author: milesws
"""
def remove_non_ascii_1(text):
    return ''.join(i for i in text if ord(i)<128)

import sys
import pandas as pd
sys.path.append(r"R:\JoePriceResearch\Python\Anaconda3\Lib\site-packages")
import jellyfish

df = pd.read_csv(r"R:\JoePriceResearch\LIFE-M\Miles Strother\Machine Learning\false_names.csv", encoding="utf-8")

df['full1'] = df['full1'].apply(remove_non_ascii_1)
df['full2'] = df['full2'].apply(remove_non_ascii_1)

df['score'] = df.apply(lambda row: jellyfish.jaro_distance(row['full1'], row['full2']), axis=1)

df = df[df.score != 1]
df = df[df.score >= .6]

del df['score']

df.to_csv(r'R:\JoePriceResearch\LIFE-M\Miles Strother\Machine Learning\false_names2.csv', head=True, encoding="utf-8")
