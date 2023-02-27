from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests
import json
import tweepy
import os 
from dotenv import load_dotenv
from .forms import NameForm
from django.core.paginator import Paginator

load_dotenv()

auth = tweepy.OAuth1UserHandler(
    os.getenv('api_key'),
    os.getenv('api_key_secret'),
    os.getenv('access_token'),
    os.getenv('access_token_secret')
)

client = tweepy.Client(bearer_token=os.getenv('bearer_token'))

api = tweepy.API(auth)

def search(x):
    tweet_search = api.search_tweets(x)

    tweets=[]

    for tweet in tweet_search:
        tweets.append(tweet.text)

    return tweets

def index(request):
    return render(request, 'index.html')

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("your_name")
            use = api.get_user(screen_name=username)
            user_tweets = client.get_users_tweets(id=use._json['id'], max_results=100)

            # tt = user_tweets[0][1]
            # print(tt)
            arr = []
            nums = []
            anchor = [None] * 100
            for i, t in enumerate(user_tweets[0]):
                check = t.text.split()
                for c in check:
                    if 'https' in c:
                        anchor[i] = c
                        nums.append(i + 1)
                        print(c)
                arr.append(" ".join(check))

            context={'data': search(username), 'tweets': arr, 'data': anchor}
    else:
        form = NameForm()

    return render(request, 'activity.html', context)
    
