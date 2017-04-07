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

fromPos = 0
output = []
score = 0
for key, word in enumerate(sentence):
    aux = np.multiply(transitions[fromPos][:], emissions[key][:])
    fromPos = np.argmax(aux)
    output.append(fromPos)
    score += aux[fromPos]

print output
