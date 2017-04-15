import numpy as np
from State import State
import copy

class GreedyDecoder:

    def __init__(self, n_prev, tag_size, K=1):
        self.K = K
        self.n_prev = n_prev
        self.tag_size = tag_size

    def setTrellis(self, trellis):
        self.trellis = trellis

    def process(self, sentence):
        self.trellis.load(sentence)

        #initState = ','.join(["-1"] * self.tag_size)
        initState = State(k=self.n_prev)
        fromPos = np.array([initState])
        output = np.array([[initState.getLastTag()]] * self.K)
        score = np.array([0] * self.K, dtype=np.float32)
        for key, word in enumerate(sentence):
            aux = np.array([], dtype=np.float32)
            for i in fromPos:
                aux = np.append(aux, self.trellis.transitions[self.trellis.getStatePosition(str(i))][:] + self.trellis.emissions[key][:])
            maximum = np.argpartition(aux, -self.K)[-self.K:]
            maximum = maximum[np.argsort(aux[maximum])] # Sort them to get the ones with highest value.

            source = maximum / self.tag_size # Determine from which sequence they came from
            destiny = maximum % self.tag_size # Determine the node they are going to
            tempOutput = np.array([None] * self.K) # Need an auxiliary variable to make the replacement
            tempScore = np.array([0] * self.K, dtype=np.float32)
            tempFromPos = np.array([None] * self.K)
            for i in range(self.K):
                tempOutput[i] = np.append(output[source[i]].copy(), destiny[i])
                tempScore[i] = score[source[i]].copy() + aux[maximum[i]]
                tempFromPos[i] = copy.copy(fromPos[source[i]])
                tempFromPos[i].push(str(destiny[i]))
            fromPos = tempFromPos
            output = tempOutput
            score = tempScore
            #print(score)

        #print score
        return output[ np.argmax(score) ][1:]
