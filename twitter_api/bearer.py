import pandas as pd
import json
import csv
import tweepy
import re
import os
from dotenv import load_dotenv
load_dotenv()


consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_KEY_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

def on_data(self, data):
    json_data = json.loads(data)
    json.dump(json_data,my_file)

for tweet in tweepy.Cursor(api.search_tweets, q='#biden').items(1):
    on_data(tweet)
    print(tweet)


