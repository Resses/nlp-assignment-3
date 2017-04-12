#!/usr/bin/python
import numpy as np
import itertools
from State import State
import copy
# I assume that a start is already provided

# Matrix with the states in the row and the tags as columns
transitions = np.array([ [0.0, 0.6, 0.4, 0.0], [0.0, 0.4, 0.2, 0.4], [0.0, 0.6, 0.1, 0.3], [0.0, 0.0, 0.0, 1.0] ])

# Matrix with the words in the row and the tags as columns
emissions = np.array([[0.0, 0.45, 0.0, 0.0], [0.0, 0.1, 0.7, 0.0], [0.0, 0.45, 0.4, 0.0], [0.0, 0.45, 0.4, 0.0], [0.0, 0.0, 0.0, 1.0] ])
#emissions = np.array([ [0.0, 0.45, 0.0, 0.0], [0.0, 0.1, 0.7, 0.0], [0.0, 0.45, 0.4, 0.0], [0.0, 0.0, 0.0, 1.0] ])

# We make sure that the start
sentence = ["Fed", "raises", "interest", "rates", "STOP"]
tags = ["^", "N", "V", "$"]

print("Transitions shape",transitions.shape)
print("Emissions shape",emissions.shape)


class Score:

    def __init__(self, score, init, statesize):
        self.score = score
        self.backpointer = [init]
        self.state = State(statesize)
        self.state.push(init)

    def addItemBackpointer(self, value):
        self.backpointer.append(value)

    def updateScore(self, value):
        self.score = value

    def pushState(self, tag):
        self.state.push(tag)

    def __str__(self):
        return "Backpointer: " + ','.join(self.backpointer) + " Score: " + str(self.score)

class Scoreboard:

    def __init__(self, statesize, tagsize):
        self.list = []
        self.list.append(Score(1, "0", statesize))
        for i in range(tagsize-1):
            self.list.append(Score(1, "0", statesize))

pos = len(sentence)-1
def pi(pos, transitions, emissions):
    'Backpointer is the sequence of positions chosen and score is the computed score for the last column'
    if pos == 0:
        scoreboard =  Scoreboard(1, 4)
    else:
        scoreboard = pi(pos-1, transitions, emissions)
    print("pos", pos)
    #if pos > 1:
    #    exit();

    tempScoreboard = copy.deepcopy(scoreboard)
    print("Scoreboard", scoreboard.list)
    # Iterate over the tags in the transition and the emissions on every tag for a given word
    # tag_dist is a list of all the transitions for all the states given tag (vector)
    # tag_given_word is the transition for a given word and tag (scalar)
    for key, (tag_dist, tag_given_word) in enumerate(list(zip(transitions.T, emissions[pos]))):
        tempScores = []
        # Iterate over all the scores to compute the new score for the current tag.
        # The scoreboard is the size of the tag list
        for key2, score in enumerate(scoreboard.list):
            #Obtain the transition for the given state and the tag
            #TODO: Check that the getStateCode's last code matches with current key.
            tag_given_state = tag_dist[score.state.getStateCode()]
            print("Tuple",score.score, tag_given_state, tag_given_word)
            tempScores.append(score.score * tag_given_state * tag_given_word)
        print("tempscores",tempScores)
        # Gets the tag that gave the highest score.
        maxpos = np.argmax(tempScores)
        print("maxpos", maxpos)
        # Push the new tag to the backpointer
        tempScoreboard.list[key].backpointer = scoreboard.list[maxpos].backpointer[:] + [str(key)]
        # Push the new tag to generate the new state
        tempScoreboard.list[key].pushState(str(key))
        tempScoreboard.list[key].updateScore(tempScores[maxpos])
        #outputScores.append(tempScores[maxpos])
    return tempScoreboard

scoreboardtest = pi(pos, transitions, emissions)
for i in scoreboardtest.list:
    print (i)
