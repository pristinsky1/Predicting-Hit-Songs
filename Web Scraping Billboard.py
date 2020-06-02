#!/usr/bin/env python
# coding: utf-8

# # Web Scraping Billboard Top 100 

# In[7]:


import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen


# In[8]:


url = 'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_1995'
html = urlopen(url) 
soup = BeautifulSoup(html, 'html.parser')


# In[11]:


tables = soup.find_all('table')
rows = [row for row in tables[0].find_all('tr')]


# In[16]:


def get_td(row):
    return [td for td in row.find_all('td')]
songs_list = [get_td(row)for row in rows[1:]]


# In[125]:


def get_artist(td):
    try:
        return td[1].a.string
    except:
        return td[1].string
def get_title(td):
    try:
        return (td[0].a.string) 
    except:
        return (td[0].string).strip('\"')
    


# In[234]:


df = pd.DataFrame(columns = ['song', 'artist'])


# In[104]:


for i in range(len(songs_list)):
    to_append = [get_title(songs_list[i]), get_artist(songs_list[i])]
    df_length = len(df)
    df.loc[df_length] = to_append


# In[106]:


#Now we need to repeat this process for every year since 1995


# In[258]:


#generate list of urls 
df = pd.DataFrame(columns = ['song', 'artist'])
urls = ['http://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{0}'.format(str(i)) for i in range(1995, 2020)]


# In[259]:


for url in urls:
    html = urlopen(url) 
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    if url.endswith('2013') or url.endswith('2012'):
        rows = [row for row in tables[1].find_all('tr')]
        songs_list = [get_td(row)for row in rows[1:]]
        for i in range(len(songs_list)):
            to_append = [get_title(songs_list[i]), get_artist(songs_list[i])]
            df_length = len(df)
            df.loc[df_length] = to_append
    else:
        rows = [row for row in tables[0].find_all('tr')]
        songs_list = [get_td(row)for row in rows[1:]]
        for i in range(len(songs_list)):
            to_append = [get_title(songs_list[i]), get_artist(songs_list[i])]
            df_length = len(df)
            df.loc[df_length] = to_append


# In[299]:


bb_hits = df
bb_hits = bb_hits.dropna()


# In[295]:


data = pd.read_csv('subset_data.csv')
data = data.drop(['id','Unnamed: 0'], axis = 1)

#add a hit column - is a hit or not
data['hit'] = 0


# In[384]:


for ind in bb_hits.index: 
    song = df['song'][ind]
    #print(song)
    if ind == 1618:
        continue
    else:
        artist = df['artist'][ind]
        to_check = data[data['name'].str.contains(song)]
        for ind, row in to_check.iterrows():
            if artist in row['artists']:
                data.loc[ind, 'hit'] = 1


# In[382]:


#Number of hits/non-hits in our dataset
data['hit'].value_counts()


# In[385]:


#Number of nulls
data.isnull().sum()


# In[389]:


data.corr()['hit']


# In[ ]:


#danceability seems to have the most affect on the popularity of a song, instrumentalness has a negative affect on it. 


# In[ ]:





# In[ ]:




