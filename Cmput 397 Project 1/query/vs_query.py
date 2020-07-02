#!/usr/bin/env python3

import sys
import os
from math import log10
from collections import defaultdict
import nltk
import json
from nltk.tokenize import RegexpTokenizer
import grab_docs as gd
import rank

def scoreQuery(termList,N,index, fromGrab):
    scores = defaultdict(int)
    outputScore = {}
    #open corpus for single token in query counts
    with open(index+"/__corpus__.json",'r') as f:
        data = json.load(f)
    for term in termList:
        scores[term] += 1
    for k,v in scores.items():
        if k in data:
            df = int(data[k]["count"])
            #calculate idf
            outputScore[k] = {'w':(log10(N/df))}
        else:
            if k in fromGrab:
                #calculate idf for phrase queries
                df = int(fromGrab[k]['count'])
                if df != 0:
                    outputScore[k] = {'w':(log10(N/df))}
                else:
                    outputScore[k] = {'w':0}
    #output the weights as {token:{w: idf}}
    return outputScore

def tknize(ls):
    #tokenize queries
    nltk_tokenizer = RegexpTokenizer(r"\w+|\$[\d\.]+|\S+^.")
    tokenizedLine = nltk_tokenizer.tokenize(ls.lower())
    return tokenizedLine

def vs_query(argv):
    #get index directory
    path = argv[0]
    N = len(os.listdir(path))-1
    numDocs = int(argv[1])
    termString = ' '.join(argv[3:])
    #tokenize terms before scoring
    temp = termString.split(' "')
    phrases = []
    regular = []
    for i in temp:
        if '"' in i:
            phrases.append(i)
        else:
            regular += i.split(' ')
    ALL = []

    for i in phrases:
        ALL+= [' '.join(tknize(i))]
    for i in regular:
        ALL+=tknize(i)

    #calling the doc grabber

    grabber = gd.DocGrabber(ALL, path)
    grabbed, grabbed4Jacy = grabber.grab_relavent()
    #getting the weighted query
    score = scoreQuery(ALL,N, path, grabbed4Jacy)
    #ranking the docs
    stuff = rank.rank(score,grabbed, numDocs)
    for thing in stuff:
        doc, score = thing
        if sys.argv[3].lower() == "y":
            print(doc +"\t" + str(score))
        else:
            print(doc)

    #send list of terms, number of docs in collection, and each terms docfrequency
    #queryTFScores = scoreQuery(tokenizedLine,N,index)
    #print(queryTFScores)

if __name__ == '__main__':
    #check if index folder exists

    if len(sys.argv) >= 5:


        if (os.path.isdir(sys.argv[1])) :
            vs_query(sys.argv[1:])
        else:
            print(sys.argv[1])
            print("Usage ./vs_query.py <index location> <number of documents to retrieve> <y/n scores> <terms> \n")
    else:
        print("Usage ./vs_query.py <index location> <number of documents to retrieve> <y/n scores> <terms> \n")
