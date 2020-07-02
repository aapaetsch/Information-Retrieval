import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
import json
from random import shuffle
from nltk.text import TextCollection as TC
import nltk.corpus
from math import log10
import numpy
import sys

def tknize(ls):
    porterStemmer = PorterStemmer()
    snowballStemmer = SnowballStemmer("english")
    engStopwords = list(set(stopwords.words('english')))
    nltk_tokenizer = RegexpTokenizer(r"\w+|\$[\d\.]+|\S+^.")
    tokenizedLine = nltk_tokenizer.tokenize(ls.lower())
    properTokenization = []
    for token in tokenizedLine:
        if (len(token) > 1) & (token not in engStopwords):
            properTokenization.append(token)

    properTokenization = [porterStemmer.stem(word) for word in properTokenization]
    properTokenization = [snowballStemmer.stem(word) for word in properTokenization]
    return properTokenization

def splitter(fileName):

    with open(fileName,'r') as f:
        d = json.load(f)
    #assuming the file is evenly divisable by 10
    for i in range(3):
        shuffle(d)
    d = d[:1000]
    corpus = []
    corpusList = []
    classifiers = []

    for i in range(len(d)):
        d[i]['tAbstract'] = tknize(d[i]['abstract'])
        corpus.extend(d[i]['tAbstract'])
        corpusList.extend(d[i]['tAbstract'])

        if d[i]['type'] not in classifiers:
            classifiers.append(d[i]['type'])

    # initialize numpy array
    for i in range(len(d)):
        d[i]['vector'] = numpy.empty([len(corpusList)])

    tc = TC(corpus)
    print("Starting vector calculation")
    for doc in d:
        place = 0
        for word in corpusList:
            idf = tc.idf(word)
            tf = tc.tf(word, doc['tAbstract'])

            # create a vector that is guaranteed to be in the same order for each doc, as
            # each doc appends the tf-idf score of the word to its vector at the same time
            doc['vector'][place] = idf * tf
            place += 1

    return d, classifiers