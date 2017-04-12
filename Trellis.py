class Trellis:

    def __init__(self):
        self.dictionary = None
        self.emission = None
        self.transition = None

    'This method loads the dictionaries for processing the sentences'
    def setDictionary(self, dictionary):
        self._resetAll()
        self.dictionary = dictionary
        self._processEmissions()

    def _resetAll(self):
        self.emission = None
        self._reset()

    'This method resets the emission and transition matrices'
    def _reset():
        self.transition = None

    'Decoders rely on knowing the start state of the dictionary'
    def getFirstState(self):
        return

    'Will generate the emission table for every state.'
    def _processEmissions(self):
        return

    '''
    Will load the references of the vectors in the dictionary object given the words
    in the sentence and create the table of distributions.
    '''
    def load(self, sentence):
        self._reset()

        for word in sentence:
            

        return
