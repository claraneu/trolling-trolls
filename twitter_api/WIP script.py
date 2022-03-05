import pandas as pd
import tweepy
import os

from dotenv import load_dotenv
load_dotenv()

consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_KEY_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

print(access_token)
hashtag_phrase = input('Keyword: ')

def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
    
    #create an authorization for accessing Twitter (aka tell the program we have permission to do what we're doing)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)

    #initiate search date variable for later timeframe specification
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
                                   lang="en", tweet_mode='extended', until=search_date).items(21):
            w.writerow([tweet.created_at,tweet.user.location, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])

    print('Done generating', hashtag_phrase, '.csv')
    return
