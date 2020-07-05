import tweepy
import pandas as pd
import csv
from src import credential
from datetime import date




def extractor(query):
    # importing credential file 
    CONSUMER_KEY = credential.api_key
    CONSUMER_SECRET = credential.api_secret_key
    ACCESS_TOKEN = credential.access_token
    ACCESS_TOKEN_SECRET= credential.access_token_secret
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    # Return API with authentication:
    api = tweepy.API(auth)
    today = date.today()
    # Open/Create a file to append data
    csvFile = open(f'./src/raw_data/tweet_{query}.csv', 'w')
    #Use csv Writer
    header = ['time','tweet']
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(header) # write header
    print('extracting tweets..........')
    for tweet in tweepy.Cursor(api.search,q=query,count=500,lang="en",since=today).items(500):
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])

    print('tweet extarcted')
    return f'./src/raw_data/tweet_{query}.csv'

    







