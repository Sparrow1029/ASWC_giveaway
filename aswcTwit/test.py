#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import twitter
import json

with open ('/home/sparrow/Documents/python_Work/twitOAuth.txt', 'r') as f:
    keys = f.read().splitlines()

api = twitter.Api(consumer_key=keys[0],
                  consumer_secret=keys[1],
                  access_token_key=keys[2],
                  access_token_secret=keys[3])


# IT'S ALIVE!
# status = api.PostUpdate('Test using python-twitter...')
# print(status.text)

# TODO: Create function to check rate limit for search? Still confused as to
#       what endpoint to ask for x-rate-limit-header...stuff...?

# Search for tweets
# These would be for using with requests/urllib:
# url = "https://api.twitter.com/1.1/search/tweets.json"
# request_method = 'GET'

hashtag = 'inktober'
num_tweets = '180'  # This is set to 180, but still only returns 100
date = '2017-10-01'


def create_query(hashtag, num_tweets, start):
    '''Function to construct query url'''
    # TODO: CLEAN vvv THIS UP...just need a start date, THEN the since_id API
    # call...probably a better way to implement.
    if type(start) is not str:
        start = str(start)
        getfield = 'l=en&q=%23'+hashtag+'&since_id='+start+'&count='+num_tweets
    getfield = 'l=en&q=%23'+hashtag+'&since%3A'+start+'&count='+num_tweets
    return getfield


# TODO: DRY this next part up.

results = api.GetSearch(raw_query=create_query(hashtag, num_tweets, date))

usr_dict = {}

for r in results:
    obj = json.loads(r.AsJsonString())

    usr_dict[obj['user']['id']] = (obj['user']['screen_name'], obj['id'])

    # print("'Tweet ID:' {}\n'User': {}, {}\n'Links': {}\n\n".format(
    # obj['id'], obj['user']['screen_name'], obj['user']['name'], obj['urls']
    # ).encode('utf-8'))

for k, v in usr_dict.items():
    print("User {}: {} -> Tweet ID: {}".format(v[0], k, v[1]))

print(len(usr_dict))  # seeing if any new ones were added

since_id = max([int(v[1]) for k, v in usr_dict.items()])
print(since_id)

nextSet = api.GetSearch(raw_query=create_query(hashtag, num_tweets, since_id))
for o in nextSet:
    j = json.loads(o.AsJsonString())
    usr_dict[j['user']['id']] = (j['user']['screen_name'], j['id'])

for k, v in usr_dict.items():
    print("User {}: {} -> Tweet ID: {}".format(v[0], k, v[1]))

print(len(usr_dict))


# TODO: select random winners?
