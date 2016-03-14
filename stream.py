# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

import sys
import unicodedata
import time

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '708346536397131776-Yts2WGbk049dA5GGTXeRpNgTcia6hqn'
ACCESS_SECRET = '4h3uCxleUKhu1hYdoOlMwHvmUFYtKjqzoLf4bZOvpNDyk'
CONSUMER_KEY = 'qV18V91EfHNjVPG7Zv4OxPl2G'
CONSUMER_SECRET = 'OqfjokvTYeQ0BQ4EV36OeCeWNYcrfKj0lhsdN4kUTUyEZAsrcW'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)
# Get the public data following through Twitter tracking the keyword
iterator = twitter_stream.statuses.filter(track=str(sys.argv[1]), language="en")

# main
cache = []          # Store words
cache_score = {}    # Store word count and time
count = 1           # number of 30 seconds
s = time.time()     # origin time
try:
    for tweet in iterator:
        try:
            line = unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore')
            line = line.split(' ')
            for i in line:
                if i in cache:
                    cache_score[i] = [cache_score[i][0] + 1, time.time()]  # increase count if present
                else:
                    cache.append(i)                                        # add word if not present 
                    cache_score[i] = [ 1 ,time.time()]

        except  KeyError :
            pass
        t = time.time()        # current time
        if t - s > count*30:
            # Decrease count for words not occuring for 30s
            for i in cache:
                if  t - cache_score[i][1] > 60:
                    cache_score[i] = [cache_score[i][0] - 1, time.time()]
                    # Deleting word from cahe if count is <= 0
                    if cache_score[i][0] <= 0:
                        del cache_score[i]
                        cache.remove(i)
            count += 1
            # for a minute interval
            if count % 2 == 1:
                # Printing words having score > 1
                for i in cache:
                    if cache_score[i][0] > 1:
                        print i
                print "$$After" , count//2 ,"minutes$$"
           
except KeyboardInterrupt:        # Ctrl + C to exit program
    pass
