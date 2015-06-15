#!/usr/bin/python

import tweepy
import ConfigParser
import sys, os

config = ConfigParser.SafeConfigParser()
config.read(os.path.join(sys.path[0], 'config'))

auth = tweepy.OAuthHandler(config.get('auth','consumer_key'), config.get('auth','consumer_secret'))
auth.set_access_token(config.get('auth','access_token'), config.get('auth','access_token_secret'))
api = tweepy.API(auth)

twitterQuery = config.get('search','query')

try:
    with open(os.path.join(sys.path[0], 'lastTweetId'), 'r') as f:
        sinceId = f.read()
except IOError:
    sinceId = ''

timelineIterator = tweepy.Cursor(api.search, q=twitterQuery, since_id=sinceId).items()

timeline = []
for status in timelineIterator:
    timeline.append(status)

try:
    lastTweetId = timeline[0].id
except IndexError:
    lastTweetId = sinceId

rtCounter = 0
errCounter = 0

timeline.reverse()

for status in timeline:
    try:
        print '(%(date)s) %(name)s: %(message)s' % \
            { 'date' : status.created_at,
            'name' : status.author.screen_name.encode('utf-8'),
            'message' : status.text.encode('utf-8') }
        api.retweet(status.id)
        rtCounter += 1
    except tweepy.error.TweepError as e:
        errCounter += 1
        print e
        continue

if errCounter != 0:
    print '%d errors occurred' % errCounter

with open(os.path.join(sys.path[0], 'lastTweetId'), 'w') as file:
    file.write(str(lastTweetId))
