#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import twitter
import json

with open ('/Users/alexray/Documents/python_work/twitOAuth.txt', 'r') as f:
    keys = f.read().splitlines()

api = twitter.Api(consumer_key=keys[0],
                  consumer_secret=keys[1],
                  access_token_key=keys[2],
                  access_token_secret=keys[3])


# IT'S ALIVE!
# status = api.PostUpdate('Test using python-twitter...')
# print(status.text)

# TODO: Search for tweets using query parameter 'our_hashtag'
#       within 7 days
url = "https://api.twitter.com/1.1/search/tweets.json"
hashtag = 'inktober'
request_method = 'GET'
getfield = 'l=en&q=%23' + hashtag + ' since%3A2017-10-01 until%3A2017-10-03'

results = api.GetSearch(raw_query=getfield)

for r in results:
    obj = json.loads(r.AsJsonString())
    print("'Tweet ID:' {}\n'User': {}, {}\n'Links': {}".format(
    obj['id'], obj['user']['screen_name'], obj['user']['name'], obj['urls']
    ).encode('utf-8'))


# TODO: Take the user_id from the returned json object and append it into
#       a dict or JSON object

# TODO: select random winners?
