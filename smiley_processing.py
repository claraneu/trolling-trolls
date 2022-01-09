print('INITIALIZING DATA PROCESSING + CLEANING')

try:
    user_csv = input('Please input the exact name of the CSV file you wish to analyze: ')
    tweet_column = input('Please input the name of the column containing the tweets: ')
    tweet_column_with_quotes = "'" + tweet_column + "'"

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
    text = re.sub(r'\!', '', text) #Remove exclamation  marks
    text = re.sub(r'\\x[a-z|A-Z|0-9]+', '', text) #Remove emojis

    return text

df_copy['tweet'] = df_copy['tweet'].apply(clean_text)

df_copy.to_csv('Cleaned_Data.csv')