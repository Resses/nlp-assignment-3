import re

class DictLowFreqClass(Dictionary):

    def __init__(self, threshold = 7):
        super(Dictionary, self).__init__()
        self.classes = ["twoDigitNum", "containsDigitAndAlpha", "initCap", "other"]
        self.regexs = [re.compile(r"(\d\d)"), re.compile(r"^(\w+-\w+)"), re.compile(r"^([A-Z]\w+)$"), re.compile(r"(.*)")]
        self.unknowns = None
        self.threshold = threshold

    '''
    This method runs over the dictionary generated with the training set, traces
    the words with the lowest frequences (less than 5). There will be a class
    used for words that can't fit any of the classes proposed. We take the words
    and add the vectors in the dictionary to the corresponding class in the
    unknown dictionary.
    '''
    def handleLowFrequencyWords(self, e):
        # Initialize the dictionary with the classes
        self.unknowns = {className: [0] * self.num_tags for className in self.classes}

        for word in e.keys():
            # Get the words with low counts
            if e[word].sum() < self.threshold:
                # Add them to the new dictionary
                self.unknowns[self.getClassForWord(word)] += e[word]
                # Remove them form the dictionary
                del e[word]

        return e

    def divideLowFrequencyWords(self, tag_counts):
        # Divide the counts(word,tag) by count(tag) and log it
        dict_size = len(self.unknowns)
        for i in range(self.num_tags):
            for word, value in self.unknowns.iteritems():
                 # We compute values using the log and also use add 1 smoothing
                self.unknowns[word][i] = np.log( (self.unknowns[word][i] + 1) / (tag_counts[i] + dict_size))

    def getClassForWord(self, word):
        for className, regExpCode in itertools.izip(self.classes, self.regexs):
            if regExpCode.search(word):
#                 if className == "other":
#                     print(word)
                return className
        return "other"

    def getEmissionsByWord(self, word):
        if self.isWordInDictionary(word):
            return self.emissions[word]
            #return super(Dictionary,self).getEmissionsByWord(word)
        else:
            return self.unknowns[self.getClassForWord(word)]
