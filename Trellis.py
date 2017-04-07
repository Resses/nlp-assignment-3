class Trellis:

    def __init__(self):
        self.dictionary = None
        self.emission = None
        self.transition = None

    'This method loads the dictionaries for processing the sentences'
    def setDictionary(self, dictionary):
        self.reset()
        self.dictionary = dictionary

    'This method resets the emission and transition matrices'
    def reset():
        self.emission = None
        self.transition = None

    def load(sentence):
        return
