# YouTube Data/Analytics API
# extracts basic stats from youtube videos: capped at 50 hits
# output dataframe variable: 'df'

# User required inputs: 
#INPUT your search name here or use the --q argument
search_term = 'Taylor Swift'
#INPUT your DEVELOPER Key: (get one here https://console.developers.google.com/project)
DEVELOPER_KEY = "insert_your_key_here" 

#import modules
from apiclient.discovery import build #pip install google-api-python-client
from apiclient.errors import HttpError 
from oauth2client.tools import argparser #pip install oauth2client
import matplotlib as plt
import pandas as pd
import argparse

#specify API
#YOUTUBE_API_SERVICE_NAME = "youtubeAnalytics"
#YOUTUBE_API_VERSION = "v1"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#allow arg replacement
argparser = argparse.ArgumentParser(conflict_handler='resolve')
#search term
argparser.add_argument("--q", help="Search term", default=search_term)

#max results returned (currently capped at 50)
argparser.add_argument("--max-results", help="Max results", default=50)
args = argparser.parse_args()
options = args

#load in parameters
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
# retrieve the search results
search_response = youtube.search().list(
 q=options.q, #artist
 type="video",
 part="id,snippet",
 maxResults=options.max_results
).execute()
videos = {} #prime dictionary

# load in the search results in for-loop
# append items of interest
 # Select only the videos: filter out channels and playlists
for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
s = ','.join(videos.keys())


#to each video extracted: add in the video statistics in dataframe format
videos_list_response = youtube.videos().list(
 id=s,
 part='id,statistics'
).execute()
res = []
for i in videos_list_response['items']:
 temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
 temp_res.update(i['statistics'])
 res.append(temp_res)

results = pd.DataFrame.from_dict(res)
print results