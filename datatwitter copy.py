#bukin dev tweet di apps.twitter.com, ajukan ke eleveted acces
#pip install tweepy

import tweepy
import re
from textblob import TextBlob

api_key = "xxxxx"
api_key_secret = "xxxxx"
access_token = "xxxxx"
access_token_secret = "xxxxx"

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#hasilUser = api.user_timeline(id="jokowi", count=10)
hasilSearch = api.search_tweets(q="jakarta", lang="en", count=100) #ubah ke id jika ingin indonesia tapi harus ditranslate

#for tweet in hasilSearch:
#  print(tweet.user.screen_name, "Ngetweet:", tweet.text)
HasilAnalisis = []

for tweet in hasilSearch:
    tweet_properties = {}
    tweet_properties["tanggal_tweet"] = tweet.created_at
    tweet_properties["pengguna"] = tweet.user.screen_name
    tweet_properties["isi_tweet"] = tweet.text
    tweet_bersih = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet.text).split())
    #print(tweet_bersih)

    analysis = TextBlob(tweet_bersih)
   # try :                                                          #untuk translate ke indo
    #    analysis = analysis.translate(to="en")
    #except Exception as e:
     #   print(e)

    if analysis.sentiment.polarity > 0.0:
        tweet_properties["sentimen"] = "positif"
    elif analysis.sentiment.polarity == 0.0:
        tweet_properties["sentimen"] = "netral" 
    else :
        tweet_properties["sentimen"] = "negatif"       

    #print(tweet_properties)

    if tweet.retweet_count > 0:
        if tweet_properties not in HasilAnalisis:
            HasilAnalisis.append(tweet_properties)
    
    else:
        HasilAnalisis.append(tweet_properties)

tweet_positif = [t for t in HasilAnalisis if t["sentimen"]=="positif"]
tweet_netral = [t for t in HasilAnalisis if t["sentimen"]=="netral"]
tweet_negatif = [t for t in HasilAnalisis if t["sentimen"]=="negatif"]

print("Hasil Sentimen")
print("positif: ", len(tweet_positif), "({} %)".format(100*len(tweet_positif)/len(HasilAnalisis)))
print("netral: ", len(tweet_netral), "({} %)".format(100*len(tweet_netral)/len(HasilAnalisis)))
print("negatif: ", len(tweet_negatif), "({} %)".format(100*len(tweet_negatif)/len(HasilAnalisis)))

print(tweet_negatif)