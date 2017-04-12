#!/usr/bin/python
import numpy as np
# I assume that a start is already provided

# Matrix with the states in the row and the tags as columns
transitions = np.array([ [0.0, 0.6, 0.4, 0.0], [0.0, 0.4, 0.2, 0.4], [0.0, 0.6, 0.1, 0.3], [0.0, 0.0, 0.0, 1.0] ])

# Matrix with the words in the row and the tags as columns
emissions = np.array([ [0.0, 0.45, 0.0, 0.0], [0.0, 0.1, 0.7, 0.0], [0.0, 0.45, 0.4, 0.0], [0.0, 0.45, 0.4, 0.0], [0.0, 0.0, 0.0, 1.0] ])

sentence = ["Fed", "raises", "interest", "rates", "STOP"]
tags = ["^", "N", "V", "$"]

print("Transitions shape",transitions.shape)
print("Emissions shape",emissions.shape)

K = 2
T = 4 # Number of tags

fromPos = np.array([0])
output = np.array([[0]] * K)
score = np.array([1] * K, dtype=np.float32)
for key, word in enumerate(sentence):
    aux = np.array([], dtype=np.float32)
    for i in fromPos:
        aux = np.append(aux, np.multiply(transitions[i][:], emissions[key][:])) # Once I use logs, function replace with addition
    maximum = np.argpartition(aux, -K)[-K:] # Determine the top K. Once I use logs, it should be the minimum
    maximum = maximum[np.argsort(aux[maximum])] # Sort them to get the ones with highest value.
    source = maximum / 4 # Determine from which sequence they came from
    destiny = maximum % 4 # Determine the node they are going to
    tempOutput = np.array([None] * K) # Need an auxiliary variable to make the replacement
    tempScore = np.array([1] * K, dtype=np.float32)
    for i in range(K):
        tempOutput[i] = np.append(output[source[i]].copy(), destiny[i])
        tempScore[i] = score[source[i]].copy() * aux[maximum[i]]
    fromPos = destiny
    output = tempOutput
    score = tempScore
    print(score)
    #fromPos = np.argmax(aux) # Once I use logs, functino replace with argmin()

print output
print score
