# Extracting Data
from datetime import datetime, timedelta
import json
import requests
import os

TIMESTAMP = '%Y-%m-%dT%H:%M:%S.00Z'
end_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP)
start_time = (datetime.now() + timedelta(-2)).date().strftime(TIMESTAMP)
query = 'Data Engineer'

tweet_fields = 'tweet.fields=author_id,created_at,id,lang,text'
user_fields = 'expansions=author_id&user.fields=id,name,username,created_at'

url_raw = f'https://api.twitter.com/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}'

os.environ['BEARER_TOKEN'] = # Insert your Twitter Dev Bearer Key

# Creating a .txt and .json File

fileName = f'collectedTweets{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.txt'
outTxt = open(fileName, 'w')
fileName = fileName.replace('.txt', '.json')
outJson = open(fileName, 'w')

# Constructing Headers

bearer_token = os.environ.get("BEARER_TOKEN")

headers = {'Authorization': f'Bearer {bearer_token}'}
response = requests.request('GET', url_raw, headers=headers)

# Storing Data

json_response = response.json()
outTxt.write(f'{json.dumps(json_response)}\n')
outJson.write(f'{json.dumps(json_response, indent=4, sort_keys=True)}\n')

while 'next_token' in json_response.get('meta', {}):
    next_token = json_response['meta']['next_token']
    url = f'{url_raw}&next_token={next_token}'
    response = requests.request('GET', url, headers=headers)
    json_response = response.json()
    outTxt.write(f'{json.dumps(json_response)}\n')
    outJson.write(f'{json.dumps(json_response, indent=4, sort_keys=True)}\n')