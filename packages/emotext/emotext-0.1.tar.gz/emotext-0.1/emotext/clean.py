import string
import re


class StringCleaning:
    """
    class for processing text data
    """

    def __init__(self, stopwods):
        self.words = ""
        self.__stop_words = []
        # read stop words
        self.__read_stopwods(stopwods)

    def __read_stopwods(self, path):
        """
        open stop words file
        """

        with open(path, "r") as files:
            for f in files.readlines():
                self.__stop_words.append(f.strip("\n"))

    def remove_char(self):
        """
        1. remove username from
        2. remove puncuation
        """

        ## remove username
        indexUser = []
        for i in range(0, len(self.words)):
            if self.words[i] == "@":
                indexUser.append(i)

        # delete username
        kata = []
        for index in indexUser:
            result = ''
            init_word = self.words[index:len(self.words)]
            for word in init_word:
                if ord(word) == 32:
                    break
                else:
                    result += word
            kata.append(result)
        
        # delete username from document
        removed_user = self.words
        for w in kata:
            removed_user = removed_user.replace(w,"")

        # remove punctuation
        for pc in string.punctuation:
            removed_user = removed_user.replace(pc,"")
        # remove all emoji
        decoded = self.__remove_stopwords(self.__emoji(removed_user))
        return decoded

    def __emoji(self, string):
        """
        remove emoji
        code reference https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
        """
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

    def fit(self, word):
        """
        fit the data to global variable
        """
        self.words = word

    def result(self):
        """
        return clean string
        """
        words = self.remove_char()
        return words.lower()

    def __remove_stopwords(self, word):
        """
        removing stop words
        """
        stopword = self.__stop_words
        kata = word.lower().split(" ")

        # free stopwords text
        clean = []
        for kt in kata:
            if kt not in stopword:
                clean.append(kt)

        # result        
        result = ''
        for text in clean:
            result += text + " "

        return result[0:len(result) - 1]