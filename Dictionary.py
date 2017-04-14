import itertools
import numpy as np

class Dictionary(object):

    def __init__(self):
        self.emissions = None
        self.transitions = None

    '''
    return all emissions (for all words,tags)
    this is structured as a dictionary where each key is a word and it's value is a numpy array with a value for each tag
    To get e(word|tag), you do emissions[word][tag]
    '''
    def getEmissions(self):
        return self.emissions

    '''returns emissions for a given word as a numpy array where each value corresponds to a tag => e(x|y) for all y values'''
    def getEmissionsByWord(self, word):
        return self.emissions[word]

    ''' Determines if the word is in the dictionary '''
    def isWordInDictionary(self, word):
        return word in self.emissions

    '''
    returns all transitions(for all states)
    this is structured as a dictionary where each key is a previous state and it's value is a numpy array with a value for each tag
    To get q(tag|prev_state), you do transitions[prev_state][tag]
    Prev_state is the previous tag in the bigram case, and previous 2 tags joined with ',' in trigram case
    '''
    def getTransitions(self):
        return self.transitions

    '''
    same as getTransitions but returns all transitions for a given state.
    '''
    def getTransitionsByState(self, prev):
        return self.transitions[prev]

    '''
    prev = previous state as string
    curr = current state (tag)
    returns q(curr|prev)
    '''
    def getTransition(self, prev, curr):
        return self.transitions[prev][curr]

    '''
    This method accepts:
        sentences - list of sentences, each represented as a list of words
        sentences_tags - tags (as #s) corresponding to the words in sentences
        tag_list - list of unique tags
        n_prev - # of previous tags to consider. 2 for trigram, 1 for bigram
    This calculates the transitions and emissions and stores them in the member variables
    '''
    def process(self, sentences, sentences_tags, tag_list, n_prev):
        self.num_tags = len(tag_list)
        self.__calculate_transitions(sentences_tags, self.num_tags, n_prev)
        self.__calculate_emissions(sentences, sentences_tags, self.num_tags)
        return

    '''
    Given the tags for each sentence and the number of unique tags,
    this method returns a dictionary where key = tag and value = tag's count
    '''
    def __calculate_tag_counts(self, sentences_tags, num_tags):
        tag_counts = [0] * num_tags
        for sent_tags in sentences_tags:
            for tag in sent_tags:
                tag_counts[tag] +=1
        return tag_counts


    def handleLowFrequencyWords(self, e):
        return e

    def divideLowFrequencyWords(self, tag_counts):
        return

    def getStatesList(self):
        return list(q.keys())

    '''
    This method, called in process, calculates the emissions,
    structured as a dictionary where each key is a word and it's value is a numpy array with a value for each tag.
    To get e(word|tag), you do e[word][tag]
    Given: list of sentences, corresponding tags, and number of unique tags
    Emissions are calculated as the log((count(word, tag) + 1) / (count(tag) + size of dictionary)) - using add-1 smoothing
    '''
    def __calculate_emissions(self, sentences, sentences_tags, num_tags):
        e = {}
        # DIEGO: This can be included within the first loop which would save an iteration over the entire set of tags.
        tag_counts = self.__calculate_tag_counts(sentences_tags, num_tags) # get dictionary of tag counts

        # First go through all words/labels and count all (word,label) pairs
        for sent, sent_tags in itertools.izip(sentences, sentences_tags):
            for word, label in itertools.izip(sent, sent_tags):
                if not word in e:
                    e[word] = np.zeros(num_tags)
                e[word][label] +=1

        'This method makes more sense when the class is extended'
        e = self.handleLowFrequencyWords(e)

        dict_size = len(e)

        # Divide the counts(word,tag) by count(tag) and log it
        for i in range(num_tags):
            for word, value in e.iteritems():
                 # We compute values using the log and also use add 1 smoothing
                e[word][i] = np.log( (e[word][i] + 1) / (tag_counts[i] + dict_size))

        # NOTE: STILL NEED TO TAKE CARE OF UNKNOWN WORDS BY DOING THE FREQUENCY THING!!!
        self.divideLowFrequencyWords(tag_counts)

        del tag_counts
        self.emissions = e
        return

    '''
    This method, called in process, calculates the transitions,
    structured as a dictionary where each key is a previous state and it's value is a numpy array with a value for each tag.
    To get q(tag|prev_state), you do transitions[prev_state][tag]
    Prev_state is the previous tag in the bigram case, and previous 2 tags joined with ',' in trigram case
    Given:
        sentences_tags - list of tags separated by sentence,
        num_tags - number of unique tags
        n - number of previous states to use. 2 for trigram, 1 for bigrram
    Transitions are calculated as the log((count(prev_state, tag) + 1) / (count(prev_state) + num_tags)) - using add-1 smoothing
    '''
    def __calculate_transitions(self, sentences_tags, num_tags, n):
        q = {}
        for state in itertools.product(range(-1,num_tags), repeat = n):
            q[','.join(str(tag) for tag in state)] = np.zeros(num_tags)

        for sent_tags in sentences_tags:  # for each sentence's list of tags
            sent_tags = ([-1] * n) + sent_tags  #appending n '-1' tags to correspond to prior states/tags for the first word(s).

            for i in range(len(sent_tags) - n):
                prior_state = ','.join(str(sent_tags[j]) for j in range(i, i + n)) # Create a string with n sequenced tags
                current_state = sent_tags[i + n]
                q[prior_state][current_state] += 1

        for prior_state, tag_list in q.iteritems():
            q[prior_state] = np.log( (tag_list + 1) / (np.sum(tag_list) + num_tags) )

        self.transitions = q
        return
