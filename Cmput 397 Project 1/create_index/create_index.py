#!/usr/bin/env python3

import sys
import os
from tokenizer import Tokenizer
from time import time
from dbCreate import corpInsert, createJSON, createCorpus, docID, folderCheck
UTILPATH = sys.path[0] + "/../util/"
sys.path.append(UTILPATH)

def create_index(argv):
    #instantiate tokenizer
    tokenizer = Tokenizer()

    #reads every file in argv[0] which should be corpus dir
    corpus = {'__total__':0} #corpus is held in memory until the final document has been indexed
    df = {}
    #50 files are tokenized and indexed into memory at a time
    files = os.listdir(argv[0]) #list all the files in a directory
    #print(files)
    N = len(files)
    folder = argv[1] #please add a folder string
    folderCheck(folder)#check if the folder exists, if not create a new one
    for file in range(N):

        try:
            if files[file].split(".")[-1] == "txt":
                #open each file and read into tokenize and dbcreate
                tokens = tokenizer.tokenize(os.path.join(argv[0], files[file]))
                #strip the doc id's
                f = docID(files[file])
                #add to the memory index and corpus

                corpus, corpusCounter =createJSON(f, tokens, folder, corpus, df)
            else:
                print("File:", files[file], "is not a valid file type.")
        except:
            print("Error: unable to open file")


    #single call for creating the corpus
    createCorpus(corpus, corpusCounter, folder)
    #adding the last bracket at the end of each token file




if __name__ == '__main__':
    #check command line arguments
    if len(sys.argv) == 3:
        create_index(sys.argv[1:])
    else:
        print("Usage: ./create_index.py <directory to be indexed> <output dir for index>\n")