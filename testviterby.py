#!/usr/bin/python
import numpy as np
import itertools
# I assume that a start is already provided

# Matrix with the states in the row and the tags as columns
transitions = np.array([ [0.0, 0.6, 0.4, 0.0], [0.0, 0.4, 0.2, 0.4], [0.0, 0.6, 0.1, 0.3], [0.0, 0.0, 0.0, 1.0] ])

# Matrix with the words in the row and the tags as columns
emissions = np.array([ [0.0, 0.45, 0.0, 0.0], [0.0, 0.1, 0.7, 0.0], [0.0, 0.45, 0.4, 0.0], [0.0, 0.45, 0.4, 0.0], [0.0, 0.0, 0.0, 1.0] ])

# We make sure that the start
sentence = ["Fed", "raises", "interest", "rates", "STOP"]
tags = ["^", "N", "V", "$"]

print("Transitions shape",transitions.shape)
print("Emissions shape",emissions.shape)


pos = len(sentence)-1
def pi(pos, transitions, emissions):
    'Backpointer is the sequence of positions chosen and score is the computed score for the last column'
    if pos == 0:
        scores, backpointers =  [1, 0, 0, 0], [[0, 0, 0, 0]]
    else:
        scores, backpointers = pi(pos-1, transitions, emissions)
    outputScores = np.array([])
    for score, backpointer, state_dist in itertools.izip(scores, backpointers, transitions):
        tempScores = []
        for tag_given_state, word_given_tag in itertools.izip(state_dist, emissions[pos]):
            tempScores.append(score * tag_given_state * word_given_tag)
        maxpos = np.argmax(tempScores)
        outputBackpointer = np.append(outputBackpointer, np.append(backpointer.copy(), maxpos))
        outputScores = np.append(outputScores, tempScores[maxpos])
    #for sentence, sent_labels in itertools.izip(sentences, labels):

    return outputScores, backpointer
