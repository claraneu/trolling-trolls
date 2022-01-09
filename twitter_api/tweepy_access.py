import json
import csv
import tweepy
import re
import os
import folium
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from datetime import date
from dotenv import load_dotenv
load_dotenv()

consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_KEY_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

#create the "until" search variable. Will be set to "today" if not specified in search function later



#before any of this, you need a Twitter Developer API. The Standard API works fine for this
#IMPORTANT: the academic API does not work with tweepy (yet?). Get the standard API and explain to Twitter, they probably won't have a problem with it

#define our function: what are we doing, what arguments do we need to do it?
def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
    
    #create an authorization for accessing Twitter (aka tell the program we have permission to do what we're doing)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)
    
    search_date = None
    if search_date == None:
     search_date = date.today()

    #make the name of the spreadsheet we will write to
    #it will be named whatever we search
    fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))
    
    #open the spreadsheet we will write to
    #with open('%s.csv' % (fname), 'w', encoding='utf-8') as file:
    with open(hashtag_phrase + '.csv', 'w', encoding='utf-8') as file:
        location_data = []
        w = csv.writer(file)

        #write header row to spreadsheet
        w.writerow(['timestamp', 'location', 'coordinates', 'tweet', 'username', 'all_hashtags', 'followers_count'])

        #for each tweet matching our hashtags, write relevant info to the spreadsheet
        #max we can pull is 500,000 tweets a month; I have it set to 100
        for tweet in tweepy.Cursor(api.search_tweets, q=hashtag_phrase+' -filter:retweets', \
                                   lang="en", tweet_mode='extended', until=search_date).items(20):
            w.writerow([tweet.created_at,tweet.user.location, tweet.coordinates, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])
            if hasattr(tweet, 'user') and hasattr(tweet.user, 'screen_name') and hasattr(tweet.user, 'location'):
                if tweet.user.location:
                    location_data.append((tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.location))
        return location_data
    

def put_markers(map, data):
    geo_locator = Nominatim(user_agent="trolling_trolls")

    for (name, location) in data:
        if location:
            try:
                location = geo_locator.geocode(location)
            except GeocoderTimedOut:
                continue
            if location:
                folium.Marker([location.latitude, location.longitude], popup=name).add_to(map)


hashtag_phrase = input('Hashtag Phrase ') #you'll enter your search terms in the form "#xyz" ; use logical operators AND/OR

if __name__ == "__main__":
    search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase)
    map = folium.Map(location=[0, 0], zoom_start=2)
    location_data = search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase)
    put_markers(map, location_data)
    map.save("index.html")
