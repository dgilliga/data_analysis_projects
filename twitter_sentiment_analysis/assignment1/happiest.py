import sys
import json
import string
import unicodedata
import re


states={'ak': 'alaska',
 'al': 'alabama',
 'ar': 'arkansas',
 'as': 'american samoa',
 'az': 'arizona',
 'ca': 'california',
 'co': 'colorado',
 'ct': 'connecticut',
 'dc': 'district of columbia',
 'de': 'delaware',
 'fl': 'florida',
 'ga': 'georgia',
 'gu': 'guam',
 'hi': 'hawaii',
 'ia': 'iowa',
 'id': 'idaho',
 'il': 'illinois',
 'in': 'indiana',
 'ks': 'kansas',
 'ky': 'kentucky',
 'la': 'louisiana',
 'ma': 'massachusetts',
 'md': 'maryland',
 'me': 'maine',
 'mi': 'michigan',
 'mn': 'minnesota',
 'mo': 'missouri',
 'mp': 'northern mariana islands',
 'ms': 'mississippi',
 'mt': 'montana',
 'na': 'national',
 'nc': 'north carolina',
 'nd': 'north dakota',
 'ne': 'nebraska',
 'nh': 'new hampshire',
 'nj': 'new jersey',
 'nm': 'new mexico',
 'nv': 'nevada',
 'ny': 'new york',
 'oh': 'ohio',
 'ok': 'oklahoma',
 'or': 'oregon',
 'pa': 'pennsylvania',
 'pr': 'puerto rico',
 'ri': 'rhode island',
 'sc': 'south carolina',
 'sd': 'south dakota',
 'tn': 'tennessee',
 'tx': 'texas',
 'ut': 'utah',
 'va': 'virginia',
 'vi': 'virgin islands',
 'vt': 'vermont',
 'wa': 'washington',
 'wi': 'wisconsin',
 'wv': 'west virginia',
 'wy': 'wyoming'
 }


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
        stateScore= {}
        for i in states.keys():
            stateScore[i] = [0]
        
        tweet  = json.loads(line)
        if 'text' in tweet.keys() and 'lang' in tweet.keys():
            if tweet['lang']=='en':  
                # remove puncutation and lower case
                tweetText = tweet['text'].translate(tblNoPunct).lower() 
                words = re.findall(r"[\w']+",tweetText)
                for word in words:
                    # do a simple match first before regex
                    if sentimentScores.has_key(word):
                        score[count] += sentimentScores[word]
                for word in words:
                    if states.has_key(word):
                        stateScore[word.encode('ascii')].append(score[count])
                    else:
                        if word in states.values():
                           stateScore[states.keys()[states.values().index(word)].encode('ascii')].append(score[count])    
            count +=1
        
    avgStateScore = {}
    maxSentiment = -1
    happiestState = 'ca'
    for i in stateScore.keys():
        sum = 0
        for j in stateScore[i]:
            sum += sum
        if sum != 0:
            avgStateScore[i] = round(float(len(stateScore[i]))/sum,2)
        else:
            avgStateScore[i] = 0
        if avgStateScore[i] > maxSentiment:
            maxSentiment = avgStateScore[i]
            happiestState = i
       
    return happiestState
def main():
    afinnfile = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sentimentScores = createSentimentScores(afinnfile)
    
    happiestState = scoreTweets(sentimentScores,tweet_file)
    
    print happiestState
    tweet_file.close()
    afinnfile.close()

if __name__ == '__main__':
    main()
