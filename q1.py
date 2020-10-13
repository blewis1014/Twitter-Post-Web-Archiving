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


consumer_key="jpP0ZPdqufGA5PBlmwCcHQGol"
consumer_secret="xWTO9duaclHAQpFNRHj4gLMyMjyi4qE3ISFbSjnTocMSYChEPp"
access_token="1618740277-HmnkAie5fcHwLp73UIDP4fMQjChbsFwm2DD83CC"
access_secret="JrwjBL6OyvRbvE2M5YxhAOEp0gh5ykgq799OiAkTP3Gnp"

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)

link_contain = set()

class StdOutListener(StreamListener):
    def __init__(self):
        super().__init__()
        self.max_tweets = 70
        self.tweet_count = 0
    
    def on_data(self,data):
        # is_retweet = False
        
        # global count
        # self.tweet_count += 1
            
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
                            # count-=1
                                self.tweet_count += 1
                                # print ("URL: %s" + r.url)
                                print ("URL"+str(self.tweet_count)+": "+ full_url)
                                link_contain.add(full_url)

                                # url_storage = open('1000URLs.txt','w')
                                # url_storage.write(full_url)
                                # url_storage.close()
                                # for tweet_url in link_contain:
                                    
                                # csvw.writerow(full_url)
                                return True
                    except Exception:
                        print("Some issue occurred; Ending process")
                        export_data(link_contain)
                        return False
                

    def on_error(self,status):
        print (status)

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
        return unshorten_url(response.getheader('Location')) 
        # return response.getheader('Location')
    else:
        return short_url

def export_data(collection):
    url_storage=open("1000URLs.txt","a")
    for url in collection:
        url_storage.write(url+"\n")
    url_storage.close()




if __name__ == '__main__':
    l = StdOutListener()
    # auth = OAuthHandler(consumer_key,consumer_secret)
    # auth.set_access_token(access_token,access_secret)
    stream = Stream(auth,l)
    # api = API(auth,)
    # csvw = csv.writer(open("1000urls.csv", "a"))

    # tags = ['Xbox']
    # stream.filter(track=tags)
    stream.filter(track=['Youtube'])
