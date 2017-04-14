import numpy as np

class GreedyDecoder:

    def __init__(self, tag_size, K=1):
        self.K = K
        self.tag_size = tag_size

    def setTrellis(self, trellis):
        self.trellis = trellis

    def process(self, sentence):
        self.trellis.load(sentence)
        self.state_size = len(self.trellis.states)
        print(self.trellis.transitions.shape)
        print(self.trellis.emissions.shape)
        #print(self.trellis.states)

        initState = ','.join(["-1"] * self.tag_size)
        print(initState)
        fromPos = np.array([self.trellis.getStatePosition(initState)])
        output = np.array([[initState]] * self.K)
        score = np.array([0] * self.K, dtype=np.float32)
        for key, word in enumerate(sentence):
            aux = np.array([], dtype=np.float32)
            for i in fromPos:
                #aux = np.append(aux, np.multiply(transitions[i][:], emissions[key][:])) # Once I use logs, function replace with addition
                aux = np.append(aux, self.trellis.transitions[i][:] + self.trellis.emissions[key][:])
            # maximum = np.argpartition(aux, -self.K)[-self.K:] # Determine the top K. Once I use logs, it should be the minimum

            #TODO: change this to minimum!!!
            maximum = np.argpartition(aux, -self.K)[-self.K:]
            maximum = maximum[np.argsort(aux[maximum])] # Sort them to get the ones with highest value.
            
            source = maximum / self.state_size # Determine from which sequence they came from
            destiny = maximum % self.state_size # Determine the node they are going to
            tempOutput = np.array([None] * self.K) # Need an auxiliary variable to make the replacement
            tempScore = np.array([0] * self.K, dtype=np.float32)
            for i in range(self.K):
                tempOutput[i] = np.append(output[source[i]].copy(), destiny[i])
                #tempScore[i] = score[source[i]].copy() * aux[maximum[i]]
                tempScore[i] = score[source[i]].copy() + aux[maximum[i]]
            fromPos = destiny
            output = tempOutput
            score = tempScore
            #print(score)

        #print output
        return output[ np.argmax(score) ]
