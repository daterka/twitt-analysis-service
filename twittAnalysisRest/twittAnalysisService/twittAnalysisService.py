from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

import nltk
# nltk.downloader.download('vader_lexicon')

class TwittAnalysisService():
    def __init__(self) -> None:
        self.noOfTweet = 10
        self.tweets = []
        self.positive = 0
        self.negative = 0
        self.neutral = 0
        self.polarity = 0
        self.tweet_list = []
        self.neutral_list = []
        self.negative_list = []
        self.positive_list = []
        self.data = None

    #Sentiment Analysis
    def percentage(self, part, whole):
        return 100 * float(part)/float(whole)

    def analyze(self, dt):
        self.data = pd.read_json (r'.\data.json')
        
        self.calcSentiments()
        self.twittListToDataframes() 

        self.calcPercentage()
 
        return self.generateResponce()

    def calcSentiments(self):
        for index, tweet in self.data.iterrows(): 
            # print(tweet)
            text = tweet['text']
            self.tweet_list.append(text)
            analysis = TextBlob(text)
            score = SentimentIntensityAnalyzer().polarity_scores(text)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            comp = score['compound']
            self.polarity += analysis.sentiment.polarity
            
            if neg > pos:
                self.negative_list.append(text)
                self.negative += 1
            elif pos > neg:
                self.positive_list.append(text)
                self.positive += 1 
            elif pos == neg:
                self.neutral_list.append(text)
                self.neutral += 1

    def twittListToDataframes(self):
        self.tweet_list = pd.DataFrame(self.tweet_list)
        self.neutral_list = pd.DataFrame(self.neutral_list)
        self.negative_list = pd.DataFrame(self.negative_list)
        self.positive_list = pd.DataFrame(self.positive_list)   

    def calcPercentage(self):
        self.positive = self.percentage(self.positive, self.noOfTweet)
        self.negative = self.percentage(self.negative, self.noOfTweet)
        self.neutral = self.percentage(self.neutral, self.noOfTweet)
        self.polarity = self.percentage(self.polarity, self.noOfTweet)

        self.positive = format(self.positive, '.1f')
        self.negative = format(self.negative, '.1f')
        self.neutral = format(self.neutral, '.1f')

    def generateResponce(self):
        all = {'total': len(self.tweet_list), 'polarity': self.polarity}
        positive = {'total': len(self.positive_list), 'polarity': self.negative}
        negative = {'total': len(self.negative_list), 'polarity': self.neutral}
        neutral = {'total': len(self.neutral_list), 'polarity': self.neutral}
        response = {'all': all, 'positive': positive, 'negative': negative, 'neutral': neutral}
        return response

TAS = TwittAnalysisService()
print(TAS.analyze(None))