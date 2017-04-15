import pandas as pd
import numpy as np
import itertools
import re

from DictLowFreqClass import DictLowFreqClass
from Dictionary import Dictionary
from Trellis import Trellis
from GreedyDecoder import GreedyDecoder

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

train_x, train_y, tag_list = read_data('data/train_x.csv', 'data/train_y.csv')
test_x = read_data('data/test_x.csv')

d = DictLowFreqClass()
d.process(train_x, train_y, tag_list, n_prev = 1)

trellis = Trellis()
greedy = GreedyDecoder(n_prev = 1, tag_size = len(tag_list), K=1)
#viterby = ViterbyDecoder()

trellis.setDictionary(d)
greedy.setTrellis(trellis)
#viterby.setTrellis(trellis)
output = []
#for sentence in test_x:

output.append( greedy.process(train_x[0]) )
    #viterbyOutput.push( viterby.process(sentence) )

#print(train_x[0])
print(output)
