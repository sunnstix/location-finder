from tweet_preprocessor import preprocessor

class PreProcess():
    def __init__(self,mode):
        self.mode = mode
        return 

    #Preprocesses tweets using tweet-preprocessor libarary!
    #Experiment with options by changing the mode parameter to a value 1-4:
    #Possible options:
    #1 - clean hashtags, mentions, and numbers
    #2 - clean mentions and numbers
    #3 - clean hashtags and numbers
    #4 - clean numbers
    def tweet_preprocessor(self, tweet_str):

        #Set to lowercase
        tweet_str = tweet_str.lower()

        #Set cleaning options
        if self.mode == 1:
            preprocessor.set_options(preprocessor.OPT.HASHTAG,
            preprocessor.OPT.MENTION,
            preprocessor.OPT.RESERVED,
            preprocessor.OPT.EMOJI,
            preprocessor.OPT.SMILEY,
            preprocessor.OPT.NUMBER)
        elif self.mode == 2:
            preprocessor.set_options(preprocessor.OPT.MENTION,
            preprocessor.OPT.RESERVED,
            preprocessor.OPT.EMOJI,
            preprocessor.OPT.SMILEY,
            preprocessor.OPT.NUMBER)
        elif self.mode == 3:
            preprocessor.set_options(preprocessor.OPT.HASHTAG,
            preprocessor.OPT.RESERVED,
            preprocessor.OPT.EMOJI,
            preprocessor.OPT.SMILEY,
            preprocessor.OPT.NUMBER)
        elif self.mode == 4:
            preprocessor.set_options(preprocessor.OPT.RESERVED,
            preprocessor.OPT.EMOJI,
            preprocessor.OPT.SMILEY,
            preprocessor.OPT.NUMBER)

        #Clean tweet
        tweet_str = preprocessor.clean(tweet_str)

        #Tokenize tweet
        tweet_str = preprocessor.tokenize(tweet_str)

        return tweet_str.split()