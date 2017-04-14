import numpy as np

class Trellis:

    def __init__(self):
        self.dictionary = None
        self.emissions = None
        self.transitions = None
        self.states = None

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
        self.states = None
        self._resetEmissions()

    'This method resets the transition matrix'
    def _resetEmissions(self):
        self.emissions = None

    '''
    Decoders rely on knowing the start state of the dictionary. This method will
    return the State object for the initialization of the algorithm.
    '''
    def getInitState(self):
        return

    def getStatePosition(self, state):
        return self.states.index(state)

    '''
    This method generates the transitions table for every tag given every state.
    This table is only required to generate once, when the dictionary is loaded.
    '''
    def _processTransitions(self):
        self.states = []
        self.transitions = []
        for key, state_dist in self.dictionary.getTransitions().iteritems():
            self.states.append(key)
            self.transitions.append(state_dist)

        self.transitions = np.array(self.transitions)
    '''
    Will load the references of the vectors in the dictionary object given the words
    in the sentence and create the table of distributions.
    '''
    def load(self, sentence):
        self._resetEmissions()
        self.emissions = []

        for word in sentence:
            self.emissions.append( self.dictionary.getEmissionsByWord(word) )

        self.emissions = np.array(self.emissions)
