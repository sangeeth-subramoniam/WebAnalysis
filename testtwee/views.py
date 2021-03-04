from django.shortcuts import render

import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import requests
import re
from bs4 import BeautifulSoup

from . import fetch
from .fetch import SentimentAnalysis

from .models import Search
from .forms import Inputform

from django.contrib.auth.decorators import login_required




@login_required
# Create your views here.
def index(request):

    historylist = []


    class Analysis:
        
        def __init__(self, term,numb):
            self.term = term
            self.number = numb
            self.sentiment = 0
            self.subjectivity = 0
            # self.url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format(self.term)
            self.url = 'https://en.wikipedia.org/wiki/{0}'.format(self.term)
            self.tweets = []
            self.tweetText = []

        def run(self):
            response = requests.get(self.url)
            # print(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            # headline_results = soup.find_all('div', class_='st')
            headline_results = soup.find_all('div', class_='mw-body-content')
            paragraphs = soup.select("p")
            length = len(paragraphs)
            print("Length = "+str(length))

            # for para in paragraphs:
            #     print('inime varum paru da ' , para.text)


            filer = open("Google.txt","a")
            if(length==0):
                length = self.number
            csvFile = open('google.csv', 'a')
            csvWriter = csv.writer(csvFile)

            polarity = 0
            positive = 0
            wpositive = 0
            spositive = 0
            negative = 0
            wnegative = 0
            snegative = 0
            neutral = 0

            print('inime dha print')


            for tweet in paragraphs:
                # Append to temp so that we can store in csv later. I use encode UTF-8
                self.tweetText.append(self.cleanTweet(str(tweet.text)).encode('utf-8'))
                # print (tweet.text.translate(non_bmp_map))    #print tweet's text
                analysis = TextBlob(tweet.text)
                # print('analysis ivan dha : ' , analysis)
                # print(analysis.sentiment)  # print tweet's polarity
                polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

                if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                    neutral += 1
                elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                    wpositive += 1
                elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                    positive += 1
                elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                    spositive += 1
                elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                    wnegative += 1
                elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                    negative += 1
                elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                    snegative += 1

            # finding average of how people are reacting
            positive = self.percentage(positive, length)
            wpositive = self.percentage(wpositive, length)
            spositive = self.percentage(spositive, length)
            negative = self.percentage(negative, length)
            wnegative = self.percentage(wnegative, length)
            snegative = self.percentage(snegative, length)
            neutral = self.percentage(neutral, length)

                # finding average reaction
            polarity = polarity / float(length)


            if (polarity == 0):
                    print("Neutral")
                    pol = "neutral"
            elif (polarity > 0 and polarity <= 0.3):
                    print("Weakly Positive")
                    pol = "Weakly Positive"
            elif (polarity > 0.3 and polarity <= 0.6):
                    print("Positive")
                    pol = "Positive"
            elif (polarity > 0.6 and polarity <= 1):
                    print("Strongly Positive")
                    pol = "Strongly Positive"

            elif (polarity > -0.3 and polarity <= 0):
                    print("Weakly Negative")
                    pol = "Weakly Negative"

            elif (polarity > -0.6 and polarity <= -0.3):
                    print("Negative")
                    pol = "Negative"
            elif (polarity > -1 and polarity <= -0.6):
                    print("Strongly Negative")
                    pol = "Strongly Negative"

            print()
            print("Detailed Report: ")
            print(str(positive) + "% people thought it was  dsfasfsda positive")
            print(str(wpositive) + "% people thought it was weakly positive")
            print(str(spositive) + "% people thought it was strongly positive")
            print(str(negative) + "% people thought it was negative")
            print(str(wnegative) + "% people thought it was weakly negative")
            print(str(snegative) + "% people thought it was strongly negative")
            print(str(neutral) + "% people thought it was neutral")
            csvWriter.writerow(self.tweetText)
            csvFile.close()

        # self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, len(headline_results))
            return [positive, wpositive, spositive, negative, wnegative, snegative, neutral, pol]

        def cleanTweet(self, tweet):

            # Remove Links, Special Characters etc from tweet
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
            # function to calculate percentage
        def percentage(self, part, whole):
                temp = 100 * float(part) / float(whole)
                return format(temp, '.2f')



    class SentimentAnalysis:

        def __init__(self):
            self.tweets = []
            self.tweetText = []

        def DownloadData(self,searchTerm,NoOfTerms):
            # authenticating
            consumerKey = 'jkupWshY89FlvOuLX0hKtDrKz'
            consumerSecret = 'bDIM0p6lnYipKWLi2gyH1MbUv1XXffZzMXMi9j7BWcy3X0Zlmp'
            accessToken = '1092682800078061568-ZJ00WOfFrxTh7abjiSytW2qe8vE6dy'
            accessTokenSecret = 'VDmXoHWlsh4m91zoZ7vDHJNTN2CiOurolMtTvXFYLvojr'
            auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
            auth.set_access_token(accessToken, accessTokenSecret)
            api = tweepy.API(auth)

            # input for term to be searched and how many tweets to search
            #searchTerm = input("Enter Keyword/Tag to search about: ")

            #NoOfTerms = int(input("Enter how many tweets to search: "))


            # searching for tweets
            self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

            # Open/create a file to append data to
            csvFile = open('tweets.csv', 'a')
            #filer = open("Tweets.txt",'a')
            #filer.write(self.tweets)
            # Use csv writer
            csvWriter = csv.writer(csvFile)


            # creating some variables to store info
            polarity = 0
            positive = 0
            wpositive = 0
            spositive = 0
            negative = 0
            wnegative = 0
            snegative = 0
            neutral = 0


            # iterating through tweets fetched
            for tweet in self.tweets:
                #Append to temp so that we can store in csv later. I use encode UTF-8
                self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                # print (tweet.text.translate(non_bmp_map))    #print tweet's text
                analysis = TextBlob(tweet.text)
                # print(analysis.sentiment)  # print tweet's polarity
                polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

                if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                    neutral += 1
                elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                    wpositive += 1
                elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                    positive += 1
                elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                    spositive += 1
                elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                    wnegative += 1
                elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                    negative += 1
                elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                    snegative += 1


            # Write to csv and close csv file
            csvWriter.writerow(self.tweetText)
            csvFile.close()
            #for twee in self.tweetText:
            #filer.write(twee.decode("UTF-8"))
            #filer.write("".join(self.tweetText))
            #filer.close()

            # finding average of how people are reacting
            positive = self.percentage(positive, NoOfTerms)
            wpositive = self.percentage(wpositive, NoOfTerms)
            spositive = self.percentage(spositive, NoOfTerms)
            negative = self.percentage(negative, NoOfTerms)
            wnegative = self.percentage(wnegative, NoOfTerms)
            snegative = self.percentage(snegative, NoOfTerms)
            neutral = self.percentage(neutral, NoOfTerms)

            # finding average reaction
            polarity = polarity / NoOfTerms

            # printing out data
            print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
            print()
            print("General Report: ")

            if (polarity == 0):
                print("Neutral")
                polt = "Neutral"
            elif (polarity > 0 and polarity <= 0.3):
                print("Weakly Positive")
                polt = "Weakly Positive"
            elif (polarity > 0.3 and polarity <= 0.6):
                print("Positive")
                polt = "Positive"
            elif (polarity > 0.6 and polarity <= 1):
                print("Strongly Positive")
                polt = "Strongly Positive"
            elif (polarity > -0.3 and polarity <= 0):
                print("Weakly Negative")
                polt = "Weakly Negative"
            elif (polarity > -0.6 and polarity <= -0.3):
                print("Negative")
                polt = "Negative"
            elif (polarity > -1 and polarity <= -0.6):
                print("Strongly Negative")
                polt = "Strongly Negative"

            print()
            print("Detailed Report: ")
            print(str(positive) + "% people thought it was tweetaatatatat positive")
            print(str(wpositive) + "% people thought it was weakly positive")
            print(str(spositive) + "% people thought it was strongly positive")
            print(str(negative) + "% people thought it was negative")
            print(str(wnegative) + "% people thought it was weakly negative")
            print(str(snegative) + "% people thought it was strongly negative")
            print(str(neutral) + "% people thought it was neutral")



            #self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)
            return [positive,wpositive,spositive,negative,wnegative,snegative,neutral, polt]


        def cleanTweet(self, tweet):
            # Remove Links, Special Characters etc from tweet
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

        # function to calculate percentage
        def percentage(self, part, whole):
            temp = 100 * float(part) / float(whole)
            return format(temp, '.2f')

        def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
            labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                    'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
            sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
            colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
            patches, texts = plt.pie(sizes, colors=colors, startangle=90)
            plt.legend(patches, labels, loc="best")
            plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
            plt.axis('equal')
            plt.tight_layout()
            plt.show()

    if(request.method == "GET"):
            history = Search.objects.all().order_by('-id')[:5]
            search = Inputform()
            return render(request, "getinput.html" , {"search_form" : search , "history" : history})

    elif(request.method == "POST"):       
        

        subject = request.POST.get('search_term')
        tweets = request.POST.get('no_of_terms')
        instancedata = Inputform(data=request.POST)

        if(instancedata.is_valid()):
            instance = instancedata.save()
            instance.save()

        # subject = "covid"
        # tweets = 50
        sa = SentimentAnalysis()
        arr = sa.DownloadData(subject,int(tweets))
        
        a = Analysis(subject,tweets)
        b = a.run()
        
        cummulation = []
        # for one, two in zip(arr,b) :
        for i in range(0,len(arr)):
            if i == 7:
                cummulation.append(b[i])
            else:
                cummulation.append(((float(arr[i])+float(b[i]))/2.0))
        
        context = {
            "result" : arr , 
            "res" : b , 
            "cum" : cummulation
        }
        print(' 1 ' , arr , ' /n 2 ' , b , ' /n 3 ' , cummulation)
        print('histlist are ', historylist)
        return render(request , 'results_combined.html', context)
        print('histlist are ', historylist)
    
    
        
    
    
    
    
    
    # result = arr,res = b, cum=cummulation


# from flask import Flask, render_template, request
# app = Flask(__name__)


    



    #if __name__== "__main__":
        #sa = SentimentAnalysis()
        #sa.DownloadData()



    # @app.route('/getForm')
    # def getForm():
    #     return render_template("TweetFormTemp.html")

    # @app.route('/getTweets', methods=['POST'])
    # def getTweets():
    #     if request.method =='POST':
    #         subject = request.form['subject']
    #         subject = "samsung"
    #         tweets = request.form['tweets']
    #         tweets = 50
    #         sa = SentimentAnalysis()
    #         arr = sa.DownloadData(subject,int(tweets))
    #         a = Analysis(subject,tweets)
    #         b = a.run()
    #         cummulation = []
    #         for one, two in zip(arr,b) :
    #             cummulation.append(((float(one)+float(two))/2.0))
    #         print("sdads")
    #         return render_template("result.html", result = arr,res = b, cum=cummulation)

    # if __name__ == '__main__':