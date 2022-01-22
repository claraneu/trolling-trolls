import json
import csv
import html
import tweepy
import re
import os
import numpy as np
# import folium
import matplotlib as plt
import pandas as pd
import seaborn as sns
# from geopy.exc import GeocoderTimedOut
# from geopy.geocoders import Nominatim
from itertools import chain
from collections import Counter
from datetime import date
from dotenv import load_dotenv
load_dotenv()

consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_KEY_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

# create the "until" search variable. Will be set to "today" if not specified in search function later


# before any of this, you need a Twitter Developer API. The Standard API works fine for this
# IMPORTANT: the academic API does not work with tweepy (yet?). Get the standard API and explain to Twitter, they probably won't have a problem with it

# define our function: what are we doing, what arguments do we need to do it?
def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):

    # create an authorization for accessing Twitter (aka tell the program we have permission to do what we're doing)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # initialize Tweepy API
    api = tweepy.API(auth)

    # dummy code to specify date input
    search_date = None
    if search_date == None:
        search_date = date.today()

    hashtags = []

    # make the name of the spreadsheet we will write to
    # it will be named whatever we search

    # open the spreadsheet we will write to
    with open(hashtag_phrase + '.csv', 'w', encoding='utf-8') as file:
        w = csv.writer(file)

        # write header row to spreadsheet
        w.writerow(['timestamp', 'location', 'tweet', 'username',
                   'all_hashtags', 'followers_count'])
        print('Created ' + hashtag_phrase + ' .csv (Original Data)')

        # for each tweet matching our hashtags, write relevant info to the spreadsheet
        for tweet in tweepy.Cursor(api.search_tweets, q=hashtag_phrase+' -filter:retweets',
                                   lang="en", tweet_mode='extended', until=search_date).items(10):
            w.writerow([tweet.created_at, tweet.user.location, tweet.full_text.replace('\n', ' ').encode(
                'utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])
            if [e['text'] for e in tweet._json['entities']['hashtags']] != []:
                hashtags.append([e['text']
                                for e in tweet._json['entities']['hashtags']])

    hashplots = dict(Counter(chain.from_iterable(hashtags)))
    print('hashplots:', hashplots)


def clean_text(text):

    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Removed mentions
    text = re.sub(r'#', '', text)  # Removed hashtags
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove the hyperlink
    text = re.sub(r'\'[\s]+', '', text)  # Remove apostrophe
    text = re.sub(r'\.\.\.', '', text)  # Remove dots
    # text = re.sub(r'\\x[a-z|A-Z|0-9]+', '', text) #Remove emojis; old version that cuts too much
    text = re.sub(r'\\x..', '', text)  # Remove emojis
    # Remove B at start of tweet and following ' or ""
    text = re.sub(r'^b[\'|"]', '', text)
    # Remove B at start of tweet; second line because I'm too lazy to figure it out rn
    text = re.sub(r'^b', '', text)
    # Remove single quotation mark from end of line
    text = re.sub(r'\'$', '', text)
    text = re.sub(r'\!', '', text)  # Remove exclamation  marks

    return text


# ask user for search term
# you'll enter your search terms in the form "#xyz" ; use logical operators AND/OR
hashtag_phrase = input('Hashtag Phrase ')

if __name__ == "__main__":
    search_for_hashtags(consumer_key, consumer_secret,
                        access_token, access_token_secret, hashtag_phrase)

try:
    # user_csv = hashtag_phrase + '.csv'

    # user_csv = input('Please input the exact name of the CSV file you wish to analyze: ')
    # tweet_column = input('Please input the name of the column containing the tweets: ')
    # tweet_column_with_quotes = "'" + tweet_column + "'"

    tweet_column = 'tweet'
    dataframe = pd.read_csv(hashtag_phrase + '.csv',
                            delimiter=',', encoding='utf-8', header=0)
    pd.set_option('display.max_colwidth', None)
    # renaming the tweet column to 'tweet'
    dataframe.rename(columns={tweet_column: 'tweet'})

except FileNotFoundError:
    print('There was an error finding the CSV you requested, please check the following:', '\n',
          '1. The CSV file is in the correct directory', '\n', '2. You gave the correct name of the file, following the syntax: yourfilename.csv')

df_copy = dataframe.copy()  # creating a copy of the dataframe
df_copy['tweet'] = df_copy['tweet'].str.lower()  # making everything lower case
df_copy.drop_duplicates(subset='tweet', keep='first',
                        inplace=True, ignore_index=False)  # removing duplicates
df_copy[~df_copy.tweet.str.startswith('rt')]  # removing retweets
df_copy['tweet'] = df_copy['tweet'].apply(
    lambda k: html.unescape(str(k)))  # removing unnecessary characters
df_copy['tweet'] = df_copy['tweet'].apply(clean_text)
df_copy['username'] = df_copy['username'].apply(
    lambda k: html.unescape(str(k)))  # removing unnecessary characters
df_copy['username'] = df_copy['username'].apply(clean_text)
df_copy['all_hashtags'] = df_copy['all_hashtags'].apply(
    lambda k: html.unescape(str(k)))  # removing unnecessary characters
df_copy['all_hashtags'] = df_copy['all_hashtags'].apply(clean_text)
df_copy.to_csv(hashtag_phrase + '_preproc.csv')
print('Created ' + hashtag_phrase + '_preproc.csv')


# %%
''''
import pandas as pd
import seaborn as sns

hashtags = []

df = pd.read_csv('biden' + '_preproc.csv', delimiter=',',
                 encoding='utf-8', header = 0)
# print(df.head())



for entry in df['all_hashtags']:
    if entry == '[]':
        continue
    else:
        hashtags.append(entry.lower())


print(hashtags)
# sns.countplot(hashtags)

# sns.countplot(data=df['all_hashtags'])
'''
# %%
