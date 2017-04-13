class Trellis:

    def __init__(self):
        self.dictionary = None
        self.emissions = None
        self.transitions = None

    'This method loads the dictionaries for processing the sentences'
    def setDictionary(self, dictionary):
        self._resetAll()
        self.dictionary = dictionary
        self._processTransitions()

    def getDictionary(self):
        return self.dictionary

    'This method resets the emission and transition matrices'
    def _resetAll(self):
        self.transitions = None
        self._resetEmissions()

    'This method resets the transition matrix'
    def _resetEmissions():
        self.emissions = None

    '''
    Decoders rely on knowing the start state of the dictionary. This method will
    return the State object for the initialization of the algorithm.
    '''
    def getInitState(self):
        return

    '''
    This method generates the transitions table for every tag given every state.
    This table is only required to generate once, when the dictionary is loaded.
    '''
    def _processTransitions(self):
        self.transitions = np.array([])
        for state_dist in self.dictionary.getTransitions():
            np.append( self.transitions, state_dist )

    '''
    Will load the references of the vectors in the dictionary object given the words
    in the sentence and create the table of distributions.
    '''
    def load(self, sentence):
        self._resetEmissions()

        for word in sentence:

        return
