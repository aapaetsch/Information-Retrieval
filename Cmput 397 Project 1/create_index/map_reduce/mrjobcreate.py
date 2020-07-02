#! /usr/bin/env python3

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol, StandardJSONProtocol
import sys
import os
import nltk
from nltk.tokenize import RegexpTokenizer
import string
from collections import defaultdict
import json
from math import log10

nltk.download('punkt')
nltk_tokenizer = RegexpTokenizer(r"\w+|\$[\d\.]+|\S+^.")

class MRIndexCreatorCorpus(MRJob):

    OUTPUT_PROTOCOL = JSONValueProtocol
    
    #maps input
    def mapper(self, _, line):
        self.increment_counter('group','num_mapper_calls',1)
        #gets doc fie name and parses out the doc ID
        inputFile = os.environ['map_input_file']
        filename = inputFile.split("/")
        filename = str(filename[-1:])
        docID = filename.split("_")
        docID = docID[1]
        #tokenizes line using nltk
        tokenized = nltk_tokenizer.tokenize(line.lower())
        #adds position to the token
        for pos, word in enumerate(tokenized):
            if len(word) == 1:
                word = word.translate(str.maketrans('','',string.punctuation))
            word = word.translate(str.maketrans("\/.", "&&,"))
            #emits the token as a key and the count,docID and position as value
            yield word.lower(), (1, docID, pos)

    #combines before hitting reducer
    def combiner(self, word, stuff):
        self.increment_counter('group','num_combiner_calls',1)  
        docDict = defaultdict(list)
        #gets the value from mapper and reduces it to create the json for the token with count and docID's list
        for value in stuff:
            count, docID, pos = value
            if docID not in docDict["docIDs"]:
                docDict["docIDs"].append(docID)
            try:
                docDict["count"] += count
            except:
                docDict["count"] = count
        #emits to reducer
        yield None, (word, docDict)
    
    #reduces the combined emit from combiner
    def reducer(self, _, fullset):
        self.increment_counter('group','num_reducer_calls',1)
        corpusCombine = {}
        #reduce everything to one json and add __total__ count to the json
        for k,v in fullset:
            try:
                corpusCombine["__total__"] += v["count"]
            except:
                corpusCombine["__total__"] = v["count"]
            try:
                #add token to corpus with its count values and its list of docIDs
                corpusCombine[k]["count"] += v["count"]
                corpusCombine[k]["docIDs"] += v["docIDs"]
                #sort the corpus
                corpusCombine[k]["docIDs"] = sorted(corpusCombine[k]["docIDs"], key = lambda k: int(k))
            except:
                corpusCombine[k] = v
        #emit and return as a single line of json with key None and value as our one line representatio of __corpus__.json
        yield None, corpusCombine

#create index files (aka. 0.json, 1.json, etc)
class MRIndexCreator(MRJob):

    OUTPUT_PROTOCOL = StandardJSONProtocol
    
    #maps input
    def mapper(self, _, line):
        #line of input is a doc .txt file
        self.increment_counter('group','num_mapper_calls',1)
        #get the docID from the input file
        inputFile = os.environ['map_input_file']
        filename = inputFile.split("/")
        filename = str(filename[-1:])
        docID = filename.split("_")
        docID = docID[1]
        #tokenize the input doc
        tokenized = nltk_tokenizer.tokenize(line.lower())
        #adds position to the token
        for pos, word in enumerate(tokenized):
            if len(word) == 1:
                word = word.translate(str.maketrans('','',string.punctuation))
            word = word.translate(str.maketrans("\/.", "&&,"))
            #emits the token as key and 1, docID and pos as value
            yield word.lower(), (1, docID, pos)

    #combines the emit from mapper
    def combiner(self, token, stuff):
        self.increment_counter('group','num_combiner_calls',1)
        docDict = defaultdict(list)
        termDict = {}
        count = 0
        #combines the tokens to a dictionary of their words and positions 
        for value in stuff:
            count, docID, pos = value
            if pos not in docDict["pos"]:
                docDict["pos"].append(pos)
            try:
                docDict["count"] += count
            except:
                docDict["count"] = count
            docDict["term"] = token
            termDict[docID] = docDict
        termDict = dict(termDict)
        #emits the docID as key and termDict as a value
        yield docID, termDict
    
    #reduces the emit from combiner
    def reducer(self, docID, fullset):
        self.increment_counter('group','num_reducer_calls',1)
        corpusCombine = {}
        dictDetails = defaultdict(list)
        #reduces everything with their docID as the key so only the positions and count of those documents get reduced in their own reducer
        for combined in fullset:
            term = combined[docID]["term"]
            dictDetails[term] = defaultdict(list)
            dictDetails[term]["pos"] += combined[docID]["pos"]
            dictDetails[term]["pos"] = sorted(dictDetails[term]["pos"], key = lambda k: int(k))
            try:
                dictDetails[term]["count"] += combined[docID]["count"]
            except:
                dictDetails[term]["count"] = combined[docID]["count"]
            dictDetails[term]["tf"] = 1+log10(dictDetails[term]["count"]) #add tf score when full count for that term in doc is all reduced
            corpusCombine[term] = dictDetails[term]
        #emits docID as the key and the corpus as the value to be printed in create_index.py
        yield docID, corpusCombine

if __name__ == '__main__':
    MRIndexCreatorCorpus.run()
    MRIndexCreator.run()