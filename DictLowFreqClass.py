from Dictionary import Dictionary

class DictLowFreqClass(Dictionary):

    def __init__(classes, threshold = 5):
        self.classes = classes
        self.unknowns = None
        self.threshold = threshold

    '''
    This method runs over the dictionary generated with the training set, traces
    the words with the lowest frequences (less than 5). There will be a class
    used for words that can't fit any of the classes proposed. We take the words
    and add the vectors in the dictionary to the corresponding class in the
    unknown dictionary.
    '''
    def handleLowFrequencyWords():
        # Initialize the dictionary with the classes
        self.unknowns = {className: 0 for className in self.classes}

        for word in self.getEmissions():
            # Get the words with low counts
            if getEmissionsByWord(word).sum() < self.threshold:
                # Remove them form the dictionary and add them to the new dictionary
                self.unknowns[self.getClassForWord(word)] += getEmissionsByWord(word)

        return

    def getClassForWord(word):
        return

    # '''
    # This method runs over the testing set. Detects words that are not in the
    # dictionary, have a regular expression and replaces them with the corresponding
    # class
    # '''
    # def preProcessTestingData(sentences):
    #     return

    def getEmissionsByWord(self, word):
        if self.isWordInDictionary(word):
            return self.emissions[word]
            #return super(Dictionary,self).getEmissionsByWord(word)
        else:
            return self.unknown[self.getClassForWord(word)]
