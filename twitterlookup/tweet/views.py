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
    # response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
    # data = response_API.text
    # json.loads(data)
    # parse_json = json.loads(data)
    # active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
    # a = 2 + 2
    # b = "Tweet info"
    # context = {"result": a, "tweet": b, "cases": active_case}
    return render(request, 'index.html')

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("your_name")
            context={'data': search(username)}
            print(username)
    else:
        form = NameForm()

    return render(request, 'activity.html', context)
    
