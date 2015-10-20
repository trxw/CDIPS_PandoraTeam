# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 03:43:12 2015

@author: Johnny

This script engineers some new features from youtube data and adds it to the current billboard master table that has aggregated data and wikipedia features.

A master table is created with the new features and random forests machine learning is applied to try to make different types of predictions.

"""
import glob
import pandas as pd
from dateutil.parser import parse
import re
import numpy as np

"""
#Goal: extract the artists' YouTube trend before and during the billboard debut
"""

#generate filename list for Omid's csvs that were extracted from YouTube (YouTube Interest Searches)
filename_list = []
for filename in glob.glob('*.csv'):
    temp = filename.split(".csv", 1)
    filename_list.append(temp[0])
    

#load the billboard data so it can be merged with YouTube data
data = pd.read_csv(r'billboard_breakthrough_artists.csv')
#sort by date so that we'll keep the earliest date(1st hit for an artist):
data['date_entered'] = data['date_entered'].apply(parse)

#clean up the name to have a common identifier
def underscoreName(name):
    s = name
    if ', The' in s:
        s = 'The ' + s[:-5]
    r = re.compile(r"\s+")
    s = r.sub("_", s) # "a\nb\nc
    return s.lower()

underscore_names = []
for i in range(0, len(data['artist_standardized'])):
    new_name = underscoreName(data['artist_standardized'][i])
    underscore_names.append(new_name)
    
#prime columns to store several datapoints centered around the debut of the song at point 'a0'
data['artist_underscore'] = underscore_names
data['b4'] = [np.nan] * len(data['artist_underscore'])
data['b3'] = [np.nan] * len(data['artist_underscore'])
data['b2'] = [np.nan] * len(data['artist_underscore'])
data['b1'] = [np.nan] * len(data['artist_underscore'])
data['a0'] = [np.nan] * len(data['artist_underscore'])
data['a1'] = [np.nan] * len(data['artist_underscore'])
data['a2'] = [np.nan] * len(data['artist_underscore'])
data['a3'] = [np.nan] * len(data['artist_underscore'])
data['a4'] = [np.nan] * len(data['artist_underscore'])
    
#find matching artist names and merge data
for i in range(0, len(data['artist_underscore'])):
    for j in filename_list:
        #if artist name matches then extract data
        if j.lower() == data['artist_underscore'][i].lower(): 
            temp_file = j + '.csv'
            
            try:
                youtube = pd.read_csv(temp_file, skiprows=4, header = 0).iloc[0:394]
                temp_date = data['date_entered'][i] #perievent date to be extracted
                
                #process dates in youtube data
                date_list = []
                for k in range(0, len(youtube)):
                    temp_str = youtube['Week'][k].split(" - ", 1)
                    new_date = parse(temp_str[1])
                    date_list.append(new_date)
                youtube['date'] = date_list
                
                for l in range(0, len(youtube)):
                    if youtube['date'][l] == temp_date:
                        try:          
                            data.set_value(i, 'b4', int(youtube.iloc[:,1][l-4]))
                            data.set_value(i, 'b3', int(youtube.iloc[:,1][l-3]))
                            data.set_value(i, 'b2', int(youtube.iloc[:,1][l-2]))
                            data.set_value(i, 'b1', int(youtube.iloc[:,1][l-1]))
                            data.set_value(i, 'a0', int(youtube.iloc[:,1][l]))
                            data.set_value(i, 'a1', int(youtube.iloc[:,1][l+1]))
                            data.set_value(i, 'a2', int(youtube.iloc[:,1][l+2]))
                            data.set_value(i, 'a3', int(youtube.iloc[:,1][l+3]))
                            data.set_value(i, 'a4', int(youtube.iloc[:,1][l+4]))
                        except:
                            print temp_date
            except:
                print temp_file
                

# In[]:
"""
#get the slope coming into the debut
"""

#import statsmodels.api as sm
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
lm = LinearRegression()

#note: sklearn requires the data shape of (row number, column number). Consider using data.reshape((row number, 1)) 

data['youtube_slope'] = [np.nan] * len(data['artist_underscore'])
for i in range(0, len(data)):
    try:
        X = np.array([1,2,3,4,5])
        y = np.array([data['b4'][i], data['b3'][i], data['b2'][i], data['b1'][i], data['a0'][i]])
        X = np.reshape(X, (5,1))
        y = np.reshape(y, (5,1))
        lm.fit(X, y)
        data.set_value(i, 'youtube_slope', lm.coef_)
    except:
        print data['b4'][i] #should print the nans only
        
# In[]
"""
#let's get the 1st week's ranking as a feature
"""

#load the original billboard data will artists from year 2000-2015
data2 = pd.read_csv(r'BillboardData_mod_2000.csv')
data2 = data2[['artist', 'track', 'x1st_week']]

#merge it with recently generated youTube data
merged = pd.merge(data, data2, how = 'left', left_on = ['artist', 'track'], right_on = ['artist', 'track'])
merged = merged.drop_duplicates()
data = merged

#fix the inf on the percent change
for i in range(0, len(data)):
    if data['percent_change'].iloc[i] == float('Inf'):
        data['percent_change'].iloc[i] = data['after'].iloc[i]


data.to_csv(r'billboard_forest_analysis.csv')

# In[]
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#explore how long song's last on the charts
#plot histogram of chart lifetime
plt.hist(data['ch'], bins = 50)
plt.xlabel('Number of weeks on the billboard chart', size = 14)
plt.title('Length of time that songs spend on billboard chart', size = 13)
plt.ylabel('frequency', size = 14)
plt.xlim([0,70])
plt.ylim([0, 125])
plt.savefig('prediction_hist2.svg', format='svg', dpi=1200, bbox_inches = 'tight')

#grouped prediction group into low and high lifetime (longevity on the billboard chart) by dividing by a threshold at the 50 percentile
data = pd.read_csv(r'billboard_forest_analysis.csv')

#redefine weeks on the billboard chart into categorical var(0 = low lifetime, 1 = high lifetime; threshold divider at the 50 percentile)
data['ch_categorical2'] = [np.nan] * len(data['artist_underscore'])
data['ch'].describe()
for i in range(0, len(data['ch'])):
    if data['ch'][i] <= 13:
        data.set_value(i, 'ch_categorical2', 0)
        continue
    if data['ch'][i] > 13:
        data.set_value(i, 'ch_categorical2', 1)
        continue

#select which columns to use as features
features = data.columns[[24, 29, 30, 38, 43, 44]] #this indexes only 
print features
print data.columns

#remove rows where a null exists in our feature column
data[features].isnull().sum()
data = data.dropna(subset = features)
data[features].isnull().sum()

#fix the inf on the percent change
for i in range(0, len(data)):
    if data['percent_change'].iloc[i] == float('Inf'):
        data['percent_change'].iloc[i] = data['after'].iloc[i]

# In[]
#start here for 'bootstrapping'
#prime lists nomenclature as predictionActual = []
highlow = []
lowlow = []
highhigh = []
lowhigh = []

for i in range(0,500):
    
    #define the training and test sets: 75% train set, 25% test set
    data['train'] = np.random.uniform(0, 1, len(data)) <= .75 
    data.head()
    
    #testing: add categoricals to predict
    cat_outcome = 'ch_categorical2'
    
    categorical_list = data[cat_outcome].tolist()
    categorical_array = np.array(categorical_list)
    print data[cat_outcome].unique()
    data.target_names = np.array(['Low lifetime', 'High lifetime'])
    data['target_names'] = pd.Categorical.from_codes(categorical_array, data.target_names)
    
    #new df for the training and test sets
    train, test = data[data['train']==True], data[data['train']==False]
    
    #apply random forest classifer, #result will vary with each run
    clf = RandomForestClassifier(n_jobs=2)
    y, _ = pd.factorize(train['target_names'])
    clf.fit(train[features], y)
    preds = data.target_names[clf.predict(test[features])]
    
    #create crosstab comparison table
    crosstab = pd.crosstab(test['target_names'], preds, rownames=['actual'], colnames=['preds'])
    print crosstab
    
    #make list for the bootstrapped data
    highlow.append(crosstab.iloc[0,0])
    lowlow.append(crosstab.iloc[0,1])
    highhigh.append(crosstab.iloc[1,0])
    lowhigh.append(crosstab.iloc[1,1])
    
    
bootstrapped_data = pd.DataFrame()
bootstrapped_data['hl'] = highlow
bootstrapped_data['ll'] = lowlow
bootstrapped_data['hh'] = highhigh
bootstrapped_data['lh'] = lowhigh

bootstrapped_data.describe()

# In[]:
#analyze/plot the data:

from scipy import stats  
for i in range(0,4):
    print stats.sem(bootstrapped_data.iloc[:,i])

importances = clf.feature_importances_
indices = np.argsort(importances)

#plot it!

ax = plt.figure().add_axes([0.1, 0.1, 0.8, 0.8])
plt.title('Feature Importances')
plt.bar(range(len(indices)), importances[indices], color='b', width=0.85, align="center")
#plt.yticks(range(len(indices)), features[indices])
plt.ylabel('Relative Importance', size = 13)
ax.set_xticklabels(['Initial Slope', 'Raw Wiki Changes', 'Initial Billboard Rank', '% change WikiViews', 'Youtube slope', 'Initial YouTube views'], rotation = 45)
labels = ['Initial Wiki Slope', 'Raw Wiki Changes', 'Initial Billboard Rank', '% change WikiViews', 'Initial Youtube slope', 'Initial YouTube Interest']
for axis in [ax.xaxis, ax.xaxis]:
    axis.set(ticks=np.arange(-.4, len(labels)), ticklabels=labels)

plt.savefig('prediction_final.svg', format='svg', dpi=1200, bbox_inches = 'tight')


# In[]
#Finally: let's make an example plot for the presentation to demonstrate what features we're looking

#get the 1st week ranking as a feature
data2 = pd.read_csv(r'BillboardData_mod_2000.csv')
data2 = data2[['artist', 'track', 'x1st_week', 'x2nd_week','x3rd_week','x4th_week']]
merged = pd.merge(data, data2, how = 'left', left_on = ['artist', 'track'], right_on = ['artist', 'track'])
merged = merged.drop_duplicates()
data = merged

#fix the inf on the percent change
for i in range(0, len(data)):
    if data['percent_change'].iloc[i] == float('Inf'):
        data['percent_change'].iloc[i] = data['after'].iloc[i]

#let's use Florence and the machine as the example!
florence = pd.read_csv(r'florence.csv', header = 0)

plt.plot(florence['weeks'][0:30], florence['billboard'][0:30], 'bs', label="Billboard Rank", )
plt.plot(florence['weeks'][0:30], florence['wiki'][0:30], 'g', label="Wikipedia Page Views")
plt.plot(florence['weeks'][0:30], florence['yt'][0:30], 'r', label="YouTube Interest (normalized)")
plt.ylim([0,230])
plt.legend(loc='upper right')
plt.title('Florence and the Machine: Stats')
plt.xlabel('Time relative to billboard debut(weeks)')

plt.savefig('prediction_florence2.png', format='png', dpi=600, bbox_inches = 'tight')