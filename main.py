sentences = read.data()
dict = Dictionary(sentences)
dict.process()

trellis = Trellis()
greedy = GreedyDecoder()
viterby = ViterbyDecoder()

trellis.setDictionary(dict)
greedy.setTrellis(trellis)
viterby.setTrellis(trellis)
for i in sentences:
    greedyOutput.push( greedy.process(sentence) )
    viterbyOutput.push( viterby.process(sentence) )
