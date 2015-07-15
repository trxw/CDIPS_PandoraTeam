#Access the Twitter API through tweepy
#Extracts some basics stats from specified users; saves output as twitter_followers.csv
#Requires your APP/outh KEY and secret

#User input: list the artists twitter account (future iteration to accept actual name/verified account?)
userlist = ['taylorswift13', 'monstersandmen']

import oauth, tweepy, sys
import pandas as pd

#Set Authorization
APP_KEY = 'insert your key'
APP_SECRET = 'insert your secret'
oauth_token = 'insert your token'
oauth_token_secret = 'insert your token secret'

global api
auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(oauth_token, oauth_token_secret)
api = tweepy.API(auth)

results = {} #prime dictionary
for names in userlist:
    user = api.get_user(names)
    results[user.screen_name] = user.name, user.followers_count, user.statuses_count, user.friends_count,  user.favourites_count, user.id_str, user.verified #add to dict definition
df = pd.DataFrame.from_dict(results, orient = 'index')
df.columns = ['name', 'followers', 'tweets', 'friends', 'favorites', 'user_id', 'verified']
df.index.names = ['user'] 

df.to_csv('twitter_stats.csv')
