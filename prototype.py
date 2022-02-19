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
import sys

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



#hashtag_phrase = input('Hashtag Phrase') #you'll enter your search terms in the form "#xyz" ; use logical operators AND/OR



#before any of this, you need a Twitter Developer API. The Standard API works fine for this
#IMPORTANT: the academic API does not work with tweepy (yet?). Get the standard API and explain to Twitter, they probably won't have a problem with it





#define our function: what are we doing, what arguments do we need to do it?
def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
    
    #create an authorization for accessing Twitter (aka tell the program we have permission to do what we're doing)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)
    
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
                                   lang="en", tweet_mode='extended').items(30):
            w.writerow([tweet.created_at,tweet.user.location, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])

    return


def predict_class(hashtag_phrase):
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

    df_copy['tweet'] = df_copy['tweet'].apply(clean_text)

    #df_copy['tweet'] = df_copy['tweet'].apply(clean_text)

    tokenizer = AutoTokenizer.from_pretrained("valhalla/distilbart-mnli-12-1")
    model = AutoModelForSequenceClassification.from_pretrained("valhalla/distilbart-mnli-12-1", device = -1)

    try:
        classifier = pipeline("zero-shot-classification", model = model, tokenizer = tokenizer, device = -1) #classifier = pipeline(task='zero-shot-classification', model=model, tokenizer=tokenizer, framework='pt')
    except RuntimeError:
        print("A runtime error occurred, check if tensorflow and pytorch are correctly installed, need to be version >= 2")

    df_original = df_copy	
    rows = df_original['tweet'].count()
    df_name = df_original.head(rows)

    candidate_labels = []
    candidate_results = []
    #racist_list = []
    #sexist_list = []
    #hatespeech_list = []
    #neutral_list = []
    #negative_list = []
    #positive_list = []
    unsure_list = []
    total_list = []

    labeled_tweets = pd.DataFrame(columns= ['Racist','Sexist','Hatespeech','Neutral','Negative','Positive'])
    

    candidate_labels = ['racist', 'sexist', 'hatespeech', 'neutral', 'negative', 'positive']
    candidate_results = [0, 0, 0, 0, 0, 0]

    unsure_counter = int(0)

    for sent in tqdm(df_name['tweet'].values):
            
        res = classifier(sent, candidate_labels, multi_label = False) #change multiclass to True for different results

        if res['labels'][0] == 'racist' and res['scores'][0] >= 0.5:
            candidate_results[0] = candidate_results[0] + 1
            #racist_list.append(sent)
            total_list.append('Racist')
        elif res['labels'][0] == 'sexist' and res['scores'][0] >= 0.5:
            candidate_results[1] = candidate_results[1] + 1
            #sexist_list.append(sent)
            total_list.append('Sexist')
        elif res['labels'][0] == 'hatespeech' and res['scores'][0] >= 0.5:
            candidate_results[2] = candidate_results[2] + 1
            #hatespeech_list.append(sent)
            total_list.append('Hatespeech')
        elif res['labels'][0] == 'neutral' and res['scores'][0] >= 0.5:
            candidate_results[3] = candidate_results[3] + 1
            #neutral_list.append(sent)
            total_list.append('Neutral')
        elif res['labels'][0] == 'negative' and res['scores'][0] >= 0.5:
            candidate_results[4] = candidate_results[4] + 1
            #negative_list.append(sent)
            total_list.append('Negative')
        elif res['labels'][0] == 'positive' and res['scores'][0] >= 0.5:
            candidate_results[5] = candidate_results[5] + 1
            #positive_list.append(sent)
            total_list.append('Posititve')
        else:
            total_list.append('Unsure')
            unsure_list.append(sent)
            unsure_counter = unsure_counter +1 



        """ elif res['labels'][0] == 'unsure' and res['scores'][0] < 0.5:
            #print(sent,'\n',res['labels'],'\n',res['scores'])
            candidate_results[6] = candidate_results[6] + 1
            unsure_list.append(sent)
            total_list.append('Unsure') """


        # if res['scores'][0] > 0.5 or res['scores'][0] < 0.5: #the code below this can be removed if you do not wish to have all of the results printed (might be useful for when the program is actually implemented)
        #     print(sent)
        #     print(res['labels'])
        #     print(res['scores'])
        #     print('\n')

   
    column_values = pd.Series(total_list)
    df_copy.insert(loc=0, column='Data Labels', value=column_values)
    data = {'labels': candidate_labels, 'values': candidate_results}
    df_frequency = pd.DataFrame(data, columns=['labels', 'values'])
    print(df_frequency.head(len(candidate_labels)))
    df_frequency.to_csv('testForMiK.csv')

    print("unsure:", str(unsure_counter))
    print()

    #print(sns.barplot(data = df_frequency, x = 'labels', y = 'values'))
    return

def clean_text(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #Removed mentions
    text = re.sub(r'#', '', text) #Removed hashtags
    text = re.sub(r'https?:\/\/\S+', '', text) #Remove the hyperlink
    text = re.sub(r'\'[\s]+', '', text) #Remove apostrophe
    text = re.sub(r'\.\.\.', '', text) #Remove dots
    text = re.sub(r'\\x..', '', text) #Remove emojis
    text = re.sub(r'^b[\'|"]', '', text) #Remove B at start of tweet and following ' or ""
    text = re.sub(r'^b', '', text) #Remove B at start of tweet; second line because I'm too lazy to figure it out rn
    text = re.sub(r'\!', '', text) #Remove exclamation  marks

    return text

def run_all():

    hashtag_phrase = sys.argv[1]

    search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase)
    
    predict_class(hashtag_phrase)

    

    
    
    sys.stdout.flush()
    return



run_all()