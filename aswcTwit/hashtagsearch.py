#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import base64
import json
# import twitter
# from time import sleep
# import os
import sys


if len(sys.argv) != 3:
    print("Usage: python3 twitsearch <searchterm> <count>")
    sys.exit(0)

q_string = str(sys.argv[1])
search_count = int(sys.argv[2])

# TODO: Check to see if count is more than 100 and set a dynamic variable to
# continue searching (up to maximum api requests which is...15?)

# api = twitter.Api(consumer_key=keys[0],
#                   consumer_secret=keys[1],
#                   access_token_key=keys[2],
#                   access_token_secret=keys[3])

with open ('/home/sparrow/Documents/python_Work/twitOAuth.txt', 'r') as f:
    keys = f.read().splitlines()

consumer_key = keys[0]
consumer_secret = keys[1]

key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)


auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}


auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

# print(auth_resp.status_code)

# print(auth_resp.json().keys())

access_token = auth_resp.json()['access_token']

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}


search_params = {
    'q': q_string,
    'result_type': 'recent',
    'count': search_count
}


search_url = '{}1.1/search/tweets.json'.format(base_url)


search_resp = requests.get(search_url, headers=search_headers, params=search_params)


print(search_resp.status_code)

tweet_data = search_resp.json()

def get_tweets(tweet_data):
    for x in tweet_data['statuses']:
        tweet = "{}\n{}\n".format(x['text'], x['created_at'])
        yield tweet

tweets = get_tweets(tweet_data)
user = ''

while user != 'q':

    user = input("'n' for next tweet; 'q' to quit.\n")
    if user == 'n':
        print(next(tweets))
    else:
        sys.exit(0)
