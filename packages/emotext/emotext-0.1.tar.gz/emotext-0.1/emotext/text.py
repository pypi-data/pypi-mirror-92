from emotext.clean import StringCleaning

class SentimentProbability:

    def __init__(self):
        self.positive_words = []
        self.negative_words = []
        self.stop_words = ""
    
    def fit(self, positive, negative, stopwords):
        """
        fit positive and negative word files to global variable
        """

        # read positive words
        with open(positive, "r") as files:
            clean_words = []
            for text in files.readlines():
                clean_words.append(text.strip("\n"))
            self.positive_words = clean_words
            files.close()
        
        # read negative words
        with open(negative, "r") as files:

            clean_words = []
            for text in files.readlines():
                clean_words.append(text.strip("\n"))

            self.negative_words = clean_words
            files.close()

        # set stop words path
        self.stop_words = stopwords

    def __probability(self, word, predictor):
        """
        calculate probability of negative, neutral and positive words
        """

        match_word = []
        for training in word:
            if training in predictor:
                match_word.append(training)
        
        prob = len(match_word) / len(word)
        return prob

    def __negative_classifier(self, word):
        """
        grouping a word to be negative
        """
        
        # negative word
        negative = []
        n_index = []
        
        for n in self.negative_words:
            prob = self.__probability(n, word)
            if prob > 0.5 and word in n:
                n_index.append(self.negative_words.index(n))
                negative.append(prob)


        # count all negative words found
        if len(negative) > 0:
            n_max = negative.index(max(negative))
            return self.negative_words[n_index[n_max]]
        else:
            return None
    
    def __positive_classifier(self, word):
        """
        grouping a word to be positive
        """
        
        # negative word
        negative = []
        n_index = []
        
        for n in self.positive_words:
            prob = self.__probability(n, word)
            if prob > 0.5 and word in n:
                n_index.append(self.positive_words.index(n))
                negative.append(prob)


        # count all negative words found
        if len(negative) > 0:
            n_max = negative.index(max(negative))
            return self.positive_words[n_index[n_max]]
        else:
            return None

    def predict(self, word):
        """
        predict word it can be negative, neutral or positive word
        """
        # initial string cleaning
        cln = StringCleaning(self.stop_words)
        cln.fit(word.lower())
        words = cln.result()

        # counter
        negative = []
        positive = []

        # process
        for w in words.split(" "):
            # check for negative word
            nc = self.__negative_classifier(w)
            if nc != None and nc not in negative:
                negative.append(nc)

            np = self.__positive_classifier(w)
            if np != None and np not in positive:
                positive.append(np)
        
        ## result
        # negative > positive = negative [0]
        # negative < positive = positive [2]
        # negative == positive == neutral [4]

        result = 0

        if len(negative) > len(positive):
            result = 0
        elif len(negative) == len(positive):
            result = 2
        else:
            result = 4

        return result
