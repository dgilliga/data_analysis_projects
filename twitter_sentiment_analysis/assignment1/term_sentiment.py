import sys
import json
import string
import unicodedata
import re



def createSentimentScores(afinnfile):
    """ Creates a dict of sentiments scores read from a file.
    
        Note: format of file must be:
            <phrase><tab><score>
        Args:
            afinnfile: filename of scores
        Returns:
            dict of phrases and scores.

    """
        
    afinnfile 
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        # convert to unicode for comparing with unicode tweets
        term = term.decode('utf-8')
        scores[term] = int(score)  # Convert the score to an integer.
    return scores


def getUnicodeTblNoPunct():
    """ Maps unicode values where punctuation is deleted
        This will be used as input to translate function to remove punctuation
        from unicode tweets so we can match our phrases in the score dictionary
        
        Returns: dict of unicode chars as both keys and values but 
        where unicode punctuation maps to None
    """
    return dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))



def scoreTweets(sentimentScores, tweet_file):
    """ Returns sentiments score of tweets read from a file.
    
        Note: format of file must be tweet json object:
            https://dev.twitter.com/overview/api/tweets
        Args:
            sentimentScores: dict of <phrase> : <score>
            tweet_file: txt file each line is json tweet.
        Returns:
            array of scores for each tweet in the file.
    """
    
    # get our unicode map for removing punctuation from tweets
    tblNoPunct = getUnicodeTblNoPunct()
    
    # get length of tweetfile to initialize our score array
    length =  len(tweet_file.readlines())
    score = [0] * length
    
    # back to start of tweet file
    tweet_file.seek(0)
    count = 0
    
    # for each line in tweet file:
    #   convert json to dict
    #   if tweet is english and has text
    #       remove punctionation and make lower case
    #   
    #       linear search the whole sentimentscore dictionary
    #       to if any of the phrases are in the tweet text
    #       if the phrase is in the tweet then increment add the phrase score 
    #       to the current score for this tweet

    for line in tweet_file:
        score[count]=0
        tweet  = json.loads(line)
        if 'text' in tweet.keys() and 'lang' in tweet.keys():
            if tweet['lang']=='en':  
                # remove puncutation and lower case
                tweetText = tweet['text'].translate(tblNoPunct).lower()
                
                for phrase in sentimentScores:
                    # do a simple match first before regex
                    if phrase in tweetText:
                        # now do a more complex match to ensure full phrase is matched properly
                        regString = '^'+phrase+' .*|.* '+phrase+'$|.* '+phrase+' .*|^'+phrase+'$'
                        regPhrase = re.compile(regString)
                        if regPhrase.match(tweetText):
                            score[count] += sentimentScores[phrase]
                            #if count >=16100:
                            #    print 'Reg Matching phrase = '  + phrase
                        #if count >=16100:
                        #    print 'Matching phrase = '  + phrase
                #if count >=16100:
                #    print 'tweetText = ' + tweetText
                #    print 'score[count] = ' + str(score[count])
                #    print 'tweet[\'lang\'] ='   + str(tweet['lang'])
                words = tweetText.split(' ')
                for word in words:
                    print word + ' ' + str(score[count])
            count +=1
            
    return score
def main():
    afinnfile = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sentimentScores = createSentimentScores(afinnfile)
    
    score = scoreTweets(sentimentScores,tweet_file)
    tweet_file.close()
    afinnfile.close()

if __name__ == '__main__':
    main()
