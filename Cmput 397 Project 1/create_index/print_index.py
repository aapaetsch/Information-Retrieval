#!/usr/bin/env python3

import sys
import os
import json

utilpath = sys.path[0] + "/../util/"
sys.path.append(utilpath)

def print_token(homeFile, token, docfreq, docs):
    #print the first line of token, df:<
    print(token + ", " + str(docfreq) + ": <")
    #print each docID it appears in, count and positions
    for doc in docs:
        #open doc 
        tokenJson = doc+".json"
        tokenFile = os.path.join(homeFile,tokenJson)
        with open(tokenFile) as tokenF:
            tokenDoc = json.load(tokenF)
        positionStr = ','.join(map(str, tokenDoc[token]['pos'])) 
        print("\t" + str(doc) + ", " + str(tokenDoc[token]['count']) + ": <" + positionStr + ">;")
    print("\t > \n",flush=True)
    


def print_index(argv):
    corpus = os.path.join(argv[0],'__corpus__.json')
        #read each table in index and print it
        #check db for tables of names and get its count from count table i need to check the schema again.
        #print in form:
            #word, count
            #<doc,docCount<positions>;
            #doc, docCount<positions>;>
    with open(corpus) as corpusF:
        corpusJSON = json.load(corpusF)
    for token in corpusJSON:
        #if the token is __total__ then skip it
        if token == "__total__":
            pass
        else:
            print_token(argv[0], token, corpusJSON[token]["count"], corpusJSON[token]["docIDs"])
                
        

if __name__ == '__main__':
    #check command line arguments are correct
    if len(sys.argv) == 2:
        print_index(sys.argv[1:])
    else:
        print("Usage: ./print_index.py <directory containing index>\n")