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
f = open("sample.txt","w")

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

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count = 140
cache = []
cache_score = {}
s = time.time()
for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    # ob = json.loads(json.dumps(tweet).strip())
    try:
        line = unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore')
        line = line.split(' ')
        for i in line:
            if i in cache:
                cache_score[i] = [cache_score[i][0] + 1, time.time()]
            else:
                cache.append(i)
                cache_score[i] = [ 1 ,time.time()]
        print cache
        print cache_score
        print len(cache)

    except UnicodeEncodeError:
        pass
    t = time.time()
    print t - s
    if t - s > 60:
        for i in cache:
            f.write(str(t - cache_score[i][1]) + "\n")
            if  t - cache_score[i][1]> 30:
                cache_score[i] = [cache_score[i][0] - 1, time.time()]
                f.write(i + str(cache_score[i]) + "\n")
        s = time.time()
        break

    # The command below will do pretty printing for JSON data, try it out
    # print json.dumps(tweet, indent=4)
       
    if tweet_count <= 0:
        break 
f.close()
print time.time() - start_time
