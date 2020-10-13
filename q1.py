import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import re
import json
import datetime
import csv
import urllib.request
import requests
import urllib.parse
import http.client
from http.client import IncompleteRead

# Keys ommitted 
consumer_key="***"
consumer_secret="***"
access_token="***"
access_secret="***"

# Handles authorization with Twitter
auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)

link_contain = set() # Collection for uri links

class StdOutListener(StreamListener):

    def __init__(self):
        super().__init__()
        self.max_tweets = 70    
        self.tweet_count = 0
    
    def on_data(self,data):
                if self.tweet_count == self.max_tweets:
                    print ("Finished")
                    export_data(link_contain)
                    return False
                else:
                    try:
                        tweet = json.loads(data)
                        for url in tweet["entities"]["urls"]:
                            tweet_url = str(url["expanded_url"])
                            r = requests.head(tweet_url, allow_redirects=True).url
                            full_url = unshorten_url(r)

                            if "https://twitter" in full_url:
                                print("----Twitter URL ommited----")
                            else:
                                self.tweet_count += 1
                                print ("URL"+str(self.tweet_count)+": "+ full_url)
                                link_contain.add(full_url)

                                return True
                    except Exception:
                        print("Some issue occurred; Ending process")
                        export_data(link_contain)
                        return False
                

    def on_error(self,status):
        print (status)

# If given a shorten url, expand to final url
def unshorten_url(short_url):
    parsed = urllib.parse.urlparse(short_url)

    if(parsed.scheme == 'https'):
        h = http.client.HTTPSConnection(parsed.netloc)
    else:
        h = http.client.HTTPConnection(parsed.netloc)

    resource = parsed.path
    if parsed.query != "": 
        resource += "?" + parsed.query
    h.request('HEAD', resource )
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return unshorten_url(response.getheader('Location')) # Recurisive call if not final location
    else:
        return short_url

def export_data(collection):
    url_storage=open("TwitterURLs.txt","a")
    for url in collection:
        url_storage.write(url+"\n")
    url_storage.close()




if __name__ == '__main__':
    l = StdOutListener()
    stream = Stream(auth,l)

    stream.filter(track=['Youtube']) # Filter Twitter posts to thosse that contain the string 'YouTube'
