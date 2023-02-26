from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests
import json
import tweepy
import os 
from dotenv import load_dotenv
from .forms import NameForm

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

            context={'data': search(username), 'tweets': user_tweets.data}
            print(user_tweets)
    else:
        form = NameForm()

    return render(request, 'activity.html', context)
    
