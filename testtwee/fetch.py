import sys,tweepy,csv,re
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt


class SentimentAnalysis:

    def __init__(self,word,numb,diction):
        print('in init')
        self.tweets = []
        self.tweetText = []
        self.searchTerm = word
        self.NoOfTerms = numb
        self.dictionary = diction

        

    def DownloadData(self):

        


        print('entering dwnld data')
        # authenticating
        consumerKey = 'jkupWshY89FlvOuLX0hKtDrKz'
        consumerSecret = 'bDIM0p6lnYipKWLi2gyH1MbUv1XXffZzMXMi9j7BWcy3X0Zlmp'
        accessToken = '1092682800078061568-ZJ00WOfFrxTh7abjiSytW2qe8vE6dy'
        accessTokenSecret = 'VDmXoHWlsh4m91zoZ7vDHJNTN2CiOurolMtTvXFYLvojr'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth , wait_on_rate_limit=True)

        # input for term to be searched and how many tweets to search
        # searchTerm = input("Enter Keyword/Tag to search about: ")

        # NoOfTerms = int(input("Enter how many tweets to search: "))

        print("recieved in dwnlddata ..... the word and numb are : ", self.searchTerm,self.NoOfTerms )


        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=(self.searchTerm), lang = "en").items(int(self.NoOfTerms))
        # Open/create a file to append data to



        # csvFile = open('result.csv', 'a')

        # Use csv writer
        # csvWriter = csv.writer(csvFile)


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
        # csvWriter.writerow(self.tweetText)
        # csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, self.NoOfTerms)
        wpositive = self.percentage(wpositive, self.NoOfTerms)
        spositive = self.percentage(spositive, self.NoOfTerms)
        negative = self.percentage(negative, self.NoOfTerms)
        wnegative = self.percentage(wnegative, self.NoOfTerms)
        snegative = self.percentage(snegative, self.NoOfTerms)
        neutral = self.percentage(neutral, self.NoOfTerms)

        # finding average reaction
        polarity = polarity / int(self.NoOfTerms)
        relpolarity = max(positive,wpositive,spositive,negative,wnegative,snegative,neutral)

        # printing out data
        print("How people are reacting on " + self.searchTerm + " by analyzing " + str(self.NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
            self.dictionary['verd'] = "neutral"

        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
            verdict = "Weakly Positive"
            self.dictionary['verd'] = "Weakly Positive"
            
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
            verdict = "Positive"
            self.dictionary['verd'] = "Positive"


        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
            verdict = "Strongly Positive"
            self.dictionary['verd'] = "Strongly Positive"

        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
            verdict = "Weakly Negative"
            self.dictionary['verd'] = "Weakly Negative"

        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
            verdict = "Negative"
            self.dictionary['verd'] = "Negative"

        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")
            verdict = "Strongly Negative"
            self.dictionary['verd'] = "Strongly Negative"

        self.dictionary['positive'] = str(positive)
        self.dictionary['wpositive'] = str(wpositive)
        self.dictionary['spositive'] = str(spositive)
        self.dictionary['negative'] = str(negative)
        self.dictionary['wnegative'] = str(wnegative)
        self.dictionary['snegative'] = str(snegative)
        self.dictionary['neutral'] = str(neutral)

        key_list = list(self.dictionary.keys())
        val_list = list(self.dictionary.values())

        position = str(max(positive,wpositive,spositive,negative,wnegative,snegative,neutral))
        # relpolarity = key_list[position]

        for key, value in self.dictionary.items():
            if position == value:
                print("the relative karan is " , key)

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        print('idhu dha da relative eey : ', relpolarity)

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, self.searchTerm, self.NoOfTerms)

        return self.dictionary


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



if __name__== "__main__":
    def do():
        print('starting init')
        sa = SentimentAnalysis()
        sa.DownloadData()