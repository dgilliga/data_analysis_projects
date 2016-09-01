import sys
import json
import string
import unicodedata
import re

def wordCount(tweet_file):
    """ Returns dict of word count.
    
        Note: format of file must be tweet json object:
            https://dev.twitter.com/overview/api/tweets
        Args:
            sentimentScores: dict of <phrase> : <score>
            tweet_file: txt file each line is json tweet.
        Returns:
            array of scores for each tweet in the file.
    """
    myWordCount = {}
    
    # for each line in tweet file:
    #   convert json to dict
    #   if tweet is english and has text
    #       remove punctionation and make lower case
    #   
    #       linear search the whole sentimentscore dictionary
    #       to if any of the phrases are in the tweet text
    #       if the phrase is in the tweet then increment add the phrase score 
    #       to the current score for this tweet

    wordCount=0
    for line in tweet_file:
        tweet  = json.loads(line)
        if 'text' in tweet.keys() and 'lang' in tweet.keys():
            if tweet['lang']=='en':  
                # remove puncutation and lower case
                tweetText = tweet['text'].lower()
                words = re.findall(r"[\w']+",tweetText)
                for word in words:
                    wordCount +=1
                    if myWordCount.has_key(word):
                        myWordCount[word] += 1
                    else:
                        myWordCount[word] = 1
     
                        
    for k in  myWordCount.keys():
        print k + ' ' + str(float(myWordCount[k])/wordCount)
        #print k + ' ' + str(myWordCount[k])
                           
    return myWordCount
def main():
    
    tweet_file = open(sys.argv[1])
    
    
    myWordCount = wordCount(tweet_file)
    
    
    tweet_file.close()

if __name__ == '__main__':
    main()
