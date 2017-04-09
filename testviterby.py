#!/usr/bin/python
import numpy as np
import itertools
from State import State
# I assume that a start is already provided

# Matrix with the states in the row and the tags as columns
transitions = np.array([ [0.0, 0.6, 0.4, 0.0], [0.0, 0.4, 0.2, 0.4], [0.0, 0.6, 0.1, 0.3], [0.0, 0.0, 0.0, 1.0] ])

# Matrix with the words in the row and the tags as columns
#emissions = np.array([ [0.0, 0.45, 0.0, 0.0], [0.0, 0.1, 0.7, 0.0], [0.0, 0.45, 0.4, 0.0], [0.0, 0.45, 0.4, 0.0], [0.0, 0.0, 0.0, 1.0] ])
emissions = np.array([ [0.0, 0.45, 0.0, 0.0], [0.0, 0.1, 0.7, 0.0], [0.0, 0.45, 0.4, 0.0], [0.0, 0.0, 0.0, 1.0] ])

# We make sure that the start
sentence = ["Fed", "raises", "interest", "STOP"]
tags = ["^", "N", "V", "$"]

print("Transitions shape",transitions.shape)
print("Emissions shape",emissions.shape)


class Score:

    def __init__(self, score, backpointer, tag):
        self.score = score
        self.backpointer = backpointer
        self.state = State()

    def addItemBackpointer(value):
        self.backpointer.append(value)

    def updateScore(value):
        self.score = value

    def pushState(tag):
        self.state.push(tag)

class Scoreboard:

    def __init__(tagsize):
        self.taglist = []
        self.taglist.append(Score("^"))

pos = len(sentence)-1
def pi(pos, transitions, emissions):
    'Backpointer is the sequence of positions chosen and score is the computed score for the last column'
    if pos == 0:
        scores, backpointers =  [1, 0, 0, 0], [[], [], [], []]
    else:
        scores, backpointers = pi(pos-1, transitions, emissions)
    print("pos", pos)
    if pos > 1:
        exit();
    outputScores = []
    outputBackpointer = []
    #for score, backpointer, state_dist in itertools.izip(scores, backpointers, transitions):
    print("Scores", scores)
    print("Backpointers", backpointers)
    #for key, (state_dist, word_given_tag) in enumerate(list(zip(transitions, emissions[pos]))):
    for tags_given_word in emissions[pos]:
        tempScores = []
        for score, backpointer, tag_given_state in list(zip(scores, backpointers, state_dist)):
            print("Tuple",score, tag_given_state, word_given_tag)
            tempScores.append(score * tag_given_state * word_given_tag)
        print("tempscores",tempScores)
        maxpos = np.argmax(tempScores)
        print("maxpos", maxpos)
        print(np.append(backpointers[maxpos][:], key))
        #outputBackpointer = np.append(outputBackpointer, np.append(backpointer.copy(), maxpos), axis=0)
        outputBackpointer.append(np.append(backpointers[maxpos][:], key))
        # outputScores = np.append(outputScores, tempScores[maxpos])
        outputScores.append(tempScores[maxpos])
    #for sentence, sent_labels in itertools.izip(sentences, labels):
    return outputScores, outputBackpointer

print (pi(pos, transitions, emissions))
