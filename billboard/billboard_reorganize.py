# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:34:43 2015

@author: Johnny
"""

"""
#Do some melting for the dates in Billboard data
#Resort so that each row is a date and rank

#   first we'll disregard the specific date and just use date_entered
#   later will adjust to actual date based on the weeks from date entered
"""

import pandas as pd

#load in the data
data2 = pd.read_csv(r'C:\Users\Johnny\Desktop\CDIPS_PandoraTeam-master (3)\most useful files for mode\BillboardData_mod_2010_withfeatured.csv')
data2.columns[0:45] #view some of the data columns


#drop some columns to exclude
data2.drop(['feat1', 'feat2', 'feat3', 'feat4', 'feat5', 'feat6', 'artist_standardized', 'artist_inverted', 'featured', 'unfeatured', 'id', 'source', 'prefix', 'b-side', 'time_source', 'time_(album)', 'artist_id', 'symbl', 'reissue', 'label/number', 'media', 'stereo_(55-68)', 'pic_sleeve', 'genre', 'comments', 'written_by', 'temp_1', 'date_peaked', 'verified'], axis=1, inplace=True)


#melt the df
maindf = pd.melt(data2, id_vars=['artist', 'track', 'date_entered', 'year', 'yearly_rank', 'ch', 'x40', 'x10', 'pk', 'high', 'album', 'explicit', 'time'])


#add featured vs not main binary
maindf['featured'] = [0] * len(maindf['track'])

#rename the columns
maindf.columns = ['artist', 'track', 'date_entered', 'year', 'yearly_rank', 'ch', 'x40', 'x10', 'pk', 'high', 'album', 'explicit', 'time', 'week', 'rank', 'featured']

#remove null artist vals
maindf = maindf[pd.notnull(maindf.artist)]

maindf.to_csv('billboard2010_2015_mainartist.csv')
    
    
  
  
# In[]
#repeat for above analysis for the feat artists

data2 = pd.read_csv(r'C:\Users\Johnny\Desktop\CDIPS_PandoraTeam-master (3)\most useful files for mode\BillboardData_mod_2010_withfeatured.csv')
data2.columns[0:45] #view some of the data columns

#data2.drop(['feat1', 'feat2', 'feat3', 'feat4', 'feat5', 'feat6', 'artist_standardized', 'artist_inverted', 'featured', 'unfeatured'], axis=1, inplace=True)

#swap out the artist or feat column that you want to keep
data2.drop(['artist', 'feat2', 'feat3', 'feat4', 'feat5', 'feat6', 'artist_standardized', 'artist_inverted', 'featured', 'unfeatured', 'id', 'source', 'prefix', 'b-side', 'time_source', 'time_(album)', 'artist_id', 'symbl', 'reissue', 'label/number', 'media', 'stereo_(55-68)', 'pic_sleeve', 'genre', 'comments', 'written_by', 'temp_1', 'date_peaked', 'verified'], axis=1, inplace=True)

#first id_var is the artist or feat artist column that you want to keep
feat1 = pd.melt(data2, id_vars=['feat1', 'track', 'date_entered', 'year', 'yearly_rank', 'ch', 'x40', 'x10', 'pk', 'high', 'album', 'explicit', 'time'])


feat1['featured'] = [1] * len(maindf['track'])
feat1.columns = ['artist', 'track', 'date_entered', 'year', 'yearly_rank', 'ch', 'x40', 'x10', 'pk', 'high', 'album', 'explicit', 'time', 'week', 'rank', 'featured']  
feat1 = feat1[pd.notnull(feat1.artist)]

feat1.to_csv('billboard2010_2015_feat1artist.csv')

# In[]

result = pd.concat([maindf, feat1, feat2, feat3, feat4, feat5, feat6])

result.to_csv('billboard2010_2015_reorganized_withfeaturedartist.csv')


# In[]

import pandas as pd
import re

result = pd.read_csv(r'billboard2010_2015_reorganized_withfeaturedartist.csv')
result = result.dropna(subset=['rank'], how='all')
result = result.reset_index() #reindex


#now let's calculate the date of the ranking

#extract the numbers from the text
week_list = result['week'].tolist()
week_extracted = []
for i in range(0, len(week_list)):
    temp = re.findall(r'[0-9]+', week_list[i])
    week_extracted.append(temp)
    
week_int = []
for vals in week_extracted:
    temp = int(vals[0])
    week_int.append(temp)
    
result['week_extracted'] = week_int
test = pd.DataFrame()
test['elapsed_time'] = week_int
result.dtypes




import datetime as dt

#get the dates
def convertDate(s):
    #fmt = '%m/%d/%y'
    fmt = "%Y-%m-%d"
    s = s.split(" ")
    s = s[0]

    try:
        return dt.datetime.strptime(s, fmt)
    except:
        return None


test['date'] = result.date_entered.apply(convertDate)

date_entered = test['date'].tolist()

#calculate the date based on the date_entered var and week var
actual_date = []
for i in range(0, len(date_entered)):
    temp_delta = week_int[i]
    temp_delta = temp_delta*7 - 7 #in weeks
    elapsed_time = dt.timedelta(days=temp_delta)
    new_time = elapsed_time + date_entered[i]
    actual_date.append(new_time)
test['corrected_date'] = actual_date

result['date'] = actual_date

result.to_csv('billboard2010_2015_reorganized.csv')

