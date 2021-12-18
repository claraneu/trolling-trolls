#write to csv#

import requests
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()

#loads bearer token from environment
bearer_token = os.environ.get('BEARER_TOKEN')
headers = {"Authorization": "Bearer {}".format(bearer_token)}

#create URL variable and json object from request
url = "https://api.twitter.com/2/tweets/search/recent?query=from:TwitterDev"
response = requests.request("GET", url, headers=headers).json()

#read data into pandas dataframe and write to csv
df = pd.DataFrame(response['data'])
df.to_csv('response_python.csv')
