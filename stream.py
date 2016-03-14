# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# some thing else 
import sys
import unicodedata
import time
#f = open("sample.txt","w")

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '708346536397131776-Yts2WGbk049dA5GGTXeRpNgTcia6hqn'
ACCESS_SECRET = '4h3uCxleUKhu1hYdoOlMwHvmUFYtKjqzoLf4bZOvpNDyk'
CONSUMER_KEY = 'qV18V91EfHNjVPG7Zv4OxPl2G'
CONSUMER_SECRET = 'OqfjokvTYeQ0BQ4EV36OeCeWNYcrfKj0lhsdN4kUTUyEZAsrcW'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)
start_time = time.time()
# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.filter(track=str(sys.argv[1]), language="en")

# main
#tweet_count = 2000
cache = []
cache_score = {}
count = 1
s = time.time()
extra_time = 0
try:
    for tweet in iterator:
        #tweet_count -= 1
        try:
            line = unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore')
            line = line.split(' ')
            extra_s = time.time()
            for i in line:
                if i in cache:
                    cache_score[i] = [cache_score[i][0] + 1, time.time()]
                else:
                    cache.append(i)
                    cache_score[i] = [ 1 ,time.time()]
            extra_time += time.time() - extra_s
            print len(cache)

        except UnicodeEncodeError or KeyError:
            pass
        t = time.time()
        print t - s, extra_time
        if t - s > count*60:
            print cache_score
            for i in cache:
                if  t - cache_score[i][1] > 30:
                    cache_score[i] = [cache_score[i][0] - 1, time.time()]
                    if cache_score[i][0] <= 0:
                        del cache_score[i]
                        cache.remove(i)
            count += 1
            print cache_score
           
        #if tweet_count <= 0:
        #    print "count over"
        #    break 
except KeyboardInterrupt:
    print time.time() - start_time
