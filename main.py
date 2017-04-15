import pandas as pd
import numpy as np
import itertools
import re
from argparse import ArgumentParser

from DictLowFreqClass import DictLowFreqClass
from Dictionary import Dictionary
from Trellis import Trellis
from GreedyDecoder import GreedyDecoder
from ViterbiDecoder import ViterbiDecoder

'''
This methods accepts:
    data - a list of words
    labels - a list of tags (as #s) corresponding to data (defaults to none for test data)
    tag_delim - the tag corresponding to -DOCSTART- that we split the tags on
    word_delim - the word to split the sentences on
Returns:
    sentences: a list of lists. Each sublist holds the words of a given sentence
    sentence_labels: a list of lists of the corresponding tags (as #s) to the sentences

NOTE: This is called within read_data
'''

def get_sentences(data, labels = None, tag_delim = 0, word_delim = '-DOCSTART-'):
    sentences = []
    for x, y in itertools.groupby(data, lambda z: z == word_delim):
        if x: sentences.append([])
        sentences[-1].extend(y)
    if labels is None:
        return sentences
    else:
        sentence_labels = []
        for x, y in itertools.groupby(labels, lambda z: z == tag_delim):
            if x: sentence_labels.append([])
            sentence_labels[-1].extend(y)
        return sentences, sentence_labels


'''
This method accepts:
    data_file and label_file (optional) - file names for words and corresponding tags
Returns:
    sentences - a list of sentences, where each sentence is represented as a list of words and begins with -DOCSTART-
    sentences_tags - a list of lists of tags corresponding to the sentences, where tags are represented as integers
    tag_list - a list of the unique tags. The index of each tag is what we replace all tags with.
            Later, we will use this list to convert number tags back to actual tags:
            tags = [tag_list[x] for x in tags]

'''
def read_data(data_file, label_file = None):
    data = pd.read_csv(data_file)
    del data['id']
    if label_file is None:
        return get_sentences(list(data['word']))
    else:
        labels = pd.read_csv(label_file)
        del labels['id']

        # convert labels to numbers and store the conversion from # back to tag in a dictionary tag_list
        labels['tag'] = labels['tag'].astype('category')
        tag_list = list(labels['tag'].cat.categories)
        docstart_tag = tag_list.index('O') # get # corresponding to tag 'O'
        labels = np.array(labels['tag'].cat.codes)
        sentences, sentences_tags = get_sentences(list(data['word']), labels, tag_delim = docstart_tag)
        return sentences, sentences_tags, tag_list

def generate_file(output, filename):
    f = open(filename,'w')
    f.write("id,tag\n")
    count = 0
    for sentence in output:
        for word in sentence:
            f.write(str(count) + ",\"" + tag_list[int(word)] + "\"\n")
            count += 1
    f.close()

parser = ArgumentParser()

parser.add_argument("-s", "--states", dest = "n_prev",
    required = True, help = "Number of states in the HMM")

parser.add_argument("-b", "--beam-width", dest = "K",
    default = 2, help = "Width of the beam search (default: 2)")

parser.add_argument('--greedy', action='store_true')
parser.add_argument('--viterby', action='store_true')

parser.add_argument("-f", "--output", dest = "filename",
    required = True, help = "Filename to store the output")


args = parser.parse_args()

n_prev = int(args.n_prev)
K = int(args.K)
if args.greedy == args.viterby:
    print("Pick an algorithm")
    exit()


'Load train and dev data'
train_x, train_y, tag_list = read_data('data/train_x.csv', 'data/train_y.csv')
dev_x, dev_y, tag_list = read_data('data/dev_x.csv', 'data/dev_y.csv')
#test_x = read_data('data/test_x.csv')

'Process the data in the dictionary'
d = DictLowFreqClass()
#d = Dictionary()
d.process(train_x, train_y, tag_list, n_prev = n_prev)

'Creates Trellis'
trellis = Trellis()
trellis.setDictionary(d)

'Loads the Greedy or the Viterbi decoder and sets the trellis'
if args.greedy:
    decoder = GreedyDecoder(n_prev = n_prev, tag_size = len(tag_list), K = K)
else:
    decoder = ViterbiDecoder(n_prev = n_prev, tag_size = len(tag_list))

decoder.setTrellis(trellis)

sequence_list = []
score_list = []
print("Processing sentences")
for key, sentence in enumerate(dev_x):
    print(key)
    sequence, score = decoder.process(sentence)
    sequence_list.append(sequence)
    score_list.append(score)


totalUnknown = 0
predictedUnknown = 0
for sentence, labels, predictions in itertools.izip(dev_x, dev_y, sequence_list):
    for word, label, prediction in itertools.izip(sentence, labels, predictions):
        if not d.isWordInDictionary(word):
            totalUnknown += 1
            if str(label) == prediction:
                predictedUnknown += 1
print("Total Unknown:" +  str(totalUnknown))
print("Predicted unknown: " + str(predictedUnknown / float(totalUnknown)))

print("Saving in " + args.filename)
generate_file(sequence_list, args.filename)
