
# Extact metric from nextbigsound for a given artist across many services and dates 
# The dates that have data vary across metric and service
# 
# Modified from nbs_api.ipynb
# 
# In[1]:

import anyjson as json
import requests
from bs4 import BeautifulSoup
#import scalpyr
import urllib
from json import load 
import pandas as pd
#from pandas import DataFrame
import numpy as np
import codecs
#from urllib import request
from urllib2 import urlopen # python 2.7 version
#import urlopen
from json import load
#import sqlite3
#import csv
#import codecs
#import cStringIO
#import sys
import hashlib

# nbs api python wrapper
from nbs_api import API
import json

#api = API("nbsmobile")
api = API("swahl")

# In[4]:

# basic musicbrainz search 
import musicbrainzngs
import sys

musicbrainzngs.set_useragent(
    "cdips-music-data-project",
    "0.1",
    'https://github.com/trxw/CDIPS_PandoraTeam',
)

# In[6]:

# combined nbs + musicbrainz aritist table
from nbs_api import API
import musicbrainzngs
import sys
api = API("nbsmobile")

queries = ['Kanye West','Lady Gaga','Taylor Swift']

musicbrainzngs.set_useragent(
    "cdips-music-data-project",
    "0.1",
    'https://github.com/trxw/CDIPS_PandoraTeam',
)

# services summary
resp = json.loads(api.servicesList())
nbs_services = {key:resp[key]['human'] for key in resp.keys()}

# dataframe
artists = pd.DataFrame()

for query in queries:
    # search artist
    try:
        resp = json.loads(api.artistSearch(query))
        #print resp
        filtresp = {key:resp[key] for key in resp.keys() if (resp[key]['music_brainz_id'] is not None) }
        print filtresp
        
        for key in filtresp.keys():
            nbs_id = key
            mbz_id = filtresp[key]['music_brainz_id']
            nbs_name = filtresp[key]['name']

            try:
                result = musicbrainzngs.get_artist_by_id(mbz_id)
            except WebServiceError as exc:
                print("Something went wrong with the request: %s" % exc)
            else:
                mbz_name = ''; mbz_name=''; country='';begin_area=''
                life_span_begin='';mbz_type='';isni_list=''
                try: 
                    mbz_name = result['artist']['name']
                except:
                    pass
                try:
                    area = result['artist']['area']['name']
                except:
                    pass
                try:
                    country = result['artist']['country']
                except:
                    pass                    
                try:
                    begin_area = result['artist']['begin-area']['name']
                except:
                    pass                    
                try:
                    life_span_begin = result['artist']['life-span']['begin']
                except:
                    pass                    
                try:
                    mbz_type = result['artist']['type']
                except:
                    pass                    
                try:
                    isni_list = result['artist']['isni-list'][0]
                except:
                    pass  
                
            # genres
            genres = json.loads(api.genresArtist(nbs_id))

            gencols = []
            genlist = []
            for i in (np.arange(5)+1):
                gencols += ['genre'+str(i)]
                try:
                    genlist += [genres.pop()['name']]
                except:
                    genlist += ['']

            acols = ['id','name','music_brainz_id','music_brainz_name',
                    'area','country','begin_area','life_span_begin',
                    'music_brainz_type','isni_list']+gencols
            art = pd.DataFrame([[nbs_id,nbs_name,mbz_id,mbz_name,
                                area,country,begin_area,life_span_begin,
                               mbz_type,isni_list]+genlist],columns=acols,index=[nbs_id])
            artists = artists.append(art)
                
    except:
        print "Error for query:", query

artists.head()


# In[9]:

# Get metric data for a single artist over a given time range

import urllib
import datetime as dt
import time
start_dt = dt.datetime(2010,1,1)
end_dt = dt.datetime(2015,7,16)

#for unix based systems only
#start = start_dt.strftime("%S")
#end = end_dt.strftime("%S")

#for windows OS
start = time.mktime(start_dt.timetuple())
end = time.mktime(end_dt.timetuple())

metric = 'all'
opts = {}
opts['start'] = start
opts['end'] = end
opts['metric'] = metric
data = urllib.urlencode(opts)
print data

artist_id='143' #taylor swift
#url_metricArtist='http://nbsmobile.api3.nextbigsound.com/metrics/artist/'
url_metricArtist='http://swahl.api3.nextbigsound.com/metrics/artist/'
url = url_metricArtist + artist_id + '.json'
#url='http://nbsmobile.api3.nextbigsound.com/metrics/artist/356.json'
print url

reader = codecs.getreader("utf-8")

response = urlopen(url,data)
json_obj = load(response)


# In[23]:

#extract services list
#services = []
#for i in range(0,len(json_obj)):
#    services.append(json_obj[i]['Service']['name'])

# In[45]:


import re
"""
Use regular expressions to change an artist name string into
a valid seatgeek slug.
"""
def cleanName(name):
    r = re.compile(r"\s+")
    s = r.sub("_", name) # "a\nb\nc
    return s.lower()
    
    
#extract the stats from each service

results = pd.DataFrame()
artist_name = artists[artists.id == artist_id].name
met_list = []
service_all = []
counter = 0 #service counter

#loop through services
for iservice in range(1,len(json_obj)):
    service = json_obj[iservice]['Service']['name'] #grab the service type
    mets = json_obj[iservice]['Metric'].keys() #grab the metrics for a service
    length_tracker = len(met_list)
    
    #loop through metrics
    for i in range(0,len(mets)): #loop through each metric
        try:  dates = sorted([int(day)*86400 for day in json_obj[iservice]['Metric'][mets[i]].keys()])
        except: break
        formattedDate = []
        for date in dates:
            formattedDate.append(dt.datetime.fromtimestamp(date).strftime('%Y%m%d'))
        counts = [json_obj[iservice]['Metric'][mets[i]][key] for key in json_obj[iservice]['Metric'][mets[i]].keys()]
        met = mets[i]  
        
        count_array = np.array(counts)
        count_array = count_array[:,None]
        count_array = np.transpose(count_array)
        if counter == 0:
            results = pd.DataFrame(count_array, index=[counter], columns=formattedDate)
        else:
            results = results.append(pd.DataFrame(count_array, index=[counter], columns=formattedDate))
        met_list.append(met)
        counter += 1
        #add service metric and artist at the end.
        
        
    service_list = [service] * (len(met_list) - length_tracker)
    service_all += service_list
        
name_artist = cleanName(artist_name[0]) #clean up the name
name_artist = [name_artist] * len(met_list) #turn into a repeating list
artist_id = [artist_name.index[0]]  * len(met_list)
results.insert(0, 'artist', name_artist)
results.insert(1, 'artist_id', artist_id)
results.insert(2, 'service', service_all)
results.insert(3, 'metric', met_list)

results.to_csv('nbs_'+ cleanName(artist_name[0]) +'.csv')
