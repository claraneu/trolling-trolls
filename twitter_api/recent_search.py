#recent search file

import requests
import os
import json
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

#DELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETE#
# bearer_token='AAAAAAAAAAAAAAAAAAAAAL9qWwEAAAAAYXjrmVLFQoHio2UGchwJLeb8g%2B0%3D9PmL4kEJ7frPJM3oqcwXeHjsgAMC1XK2YbXIDYPfXx1p07OD0x'

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
