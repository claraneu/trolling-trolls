import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import torch
import html
import re
import json
import csv
import tweepy
import re
import os
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import BartTokenizer, BartModel
from transformers import pipeline
from dotenv import load_dotenv
from tqdm import tqdm
load_dotenv()

consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_KEY_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')



#before any of this, you need a Twitter Developer API. The Standard API works fine for this
#IMPORTANT: the academic API does not work with tweepy (yet?). Get the standard API and explain to Twitter, they probably won't have a problem with it

#define our function: what are we doing, what arguments do we need to do it?
def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
    
    #create an authorization for accessing Twitter (aka tell the program we have permission to do what we're doing)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)

    #sets search date. needs to be fixed, in current state useless
    search_date = None
    if search_date == None:
     search_date = date.today()

    #make the name of the spreadsheet we will write to
    #it will be named whatever we search
    """  fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))"""

    #open the spreadsheet we will write to
    """ with open('%s.csv' % (fname), 'w', encoding='utf-8') as file: """
    with open(hashtag_phrase + '.csv', 'w', encoding='utf-8') as file:

        w = csv.writer(file)

        #write header row to spreadsheet
        w.writerow(['timestamp', 'location', 'tweet', 'username', 'all_hashtags', 'followers_count'])

        #for each tweet matching our hashtags, write relevant info to the spreadsheet
        #max we can pull is 500,000 tweets a month; I have it set to 100
        for tweet in tweepy.Cursor(api.search_tweets, q=hashtag_phrase+' -filter:retweets', \
                                   lang="en", tweet_mode='extended', until=search_date).items(10):
            w.writerow([tweet.created_at,tweet.user.location, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])

    
hashtag_phrase = input('Hashtag Phrase ') #you'll enter your search terms in the form "#xyz" ; use logical operators AND/OR

if __name__ == '__main__':
    search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase)

try:
    user_csv = hashtag_phrase + '.csv'
    tweet_column = 'tweet'
    #user_csv = input('Please input the exact name of the CSV file you wish to analyze: ')
    #tweet_column = input('Please input the name of the column containing the tweets: ')
    #tweet_column_with_quotes = "'" + tweet_column + "'"

    dataframe = pd.read_csv(user_csv, delimiter=',',encoding='utf-8', header = 0)
    pd.set_option('display.max_colwidth', None)
    dataframe.rename(columns={tweet_column:'tweet'}) #renaming the tweet column to 'tweet'
    
    

except FileNotFoundError:
    print('There was an error finding the CSV you requested, please check the following:','\n', '1. The CSV file is in the correct directory', '\n', '2. You gave the correct name of the file, following the syntax: yourfilename.csv')


df_copy = dataframe.copy() #creating a copy of the dataframe
df_copy['tweet'] = df_copy['tweet'].str.lower() #making everything lower case
df_copy.drop_duplicates(subset='tweet', keep='first', inplace=True, ignore_index=False) #removing duplicates
df_copy[~df_copy.tweet.str.startswith('rt')] #removing retweets
df_copy['tweet'] = df_copy['tweet'].apply(lambda k: html.unescape(str(k))) #removing unnecessary characters

def clean_text(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #Removed mentions
    text = re.sub(r'#', '', text) #Removed hashtags
    text = re.sub(r'https?:\/\/\S+', '', text) #Remove the hyperlink
    text = re.sub(r'\'[\s]+', '', text) #Remove apostrophe
    text = re.sub(r'\...+', '', text) #Remove dots
    text = re.sub(r'\\x[a-z|A-Z|0-9]+', '', text) #Remove emojis
    text = re.sub(r'\!', '', text) #Remove exclamation  marks

    return text

df_copy['tweet'] = df_copy['tweet'].apply(clean_text)

tokenizer = AutoTokenizer.from_pretrained("valhalla/distilbart-mnli-12-1")
model = AutoModelForSequenceClassification.from_pretrained("valhalla/distilbart-mnli-12-1", device = -1)

try:
    classifier = pipeline("zero-shot-classification", model = model, tokenizer = tokenizer, device = -1) #classifier = pipeline(task='zero-shot-classification', model=model, tokenizer=tokenizer, framework='pt')
except RuntimeError:
    print("A runtime error occurred, check if tensorflow and pytorch are correctly installed, need to be version >= 2")

df_original  = df_copy	
rows = df_original['tweet'].count()
df_name = df_original.head(rows)


candidate_labels = []
candidate_results = []

candidate_labels = ['racist', 'sexist', 'hatespeech', 'neutral', 'negative', 'positive']
candidate_results = [0, 0, 0, 0, 0, 0]

for sent in tqdm(df_name['tweet'].values):
        
    res = classifier(sent, candidate_labels, multi_class = False) #change multiclass to True for different results

    if res['labels'][0] == 'racist' and res['scores'][0] > 0.5:
        candidate_results[0] = candidate_results[0] + 1
    if res['labels'][0] == 'sexist' and res['scores'][0] > 0.5:
        candidate_results[1] = candidate_results[1] + 1
    if res['labels'][0] == 'hatespeech' and res['scores'][0] > 0.5:
        candidate_results[2] = candidate_results[2] + 1
    if res['labels'][0] == 'neutral' and res['scores'][0] > 0.5:
        candidate_results[3] = candidate_results[3] + 1
    if res['labels'][0] == 'negative' and res['scores'][0] > 0.5:
        candidate_results[4] = candidate_results[4] + 1
    if res['labels'][0] == 'positive' and res['scores'][0] > 0.5:
        candidate_results[5] = candidate_results[5] + 1

"""     if res['scores'][0] > 0.5: #the code below this can be removed if you do not wish to have all of the results printed (might be useful for when the program is actually implemented)
        print(sent)
        print(res['labels'])
        print(res['scores'])
        print('\n')
 """
data = {'labels': candidate_labels, 'values': candidate_results}
df_frequency = pd.DataFrame(data, columns=['labels', 'values'])
print(df_frequency.head(len(candidate_labels)))
print(sns.barplot(data = df_frequency, x = 'labels', y = 'values'))