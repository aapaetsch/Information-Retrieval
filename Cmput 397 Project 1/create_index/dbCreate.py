import numpy as np
import os
import json
from math import log10

def corpInsert(corp, key, dID, df, count):
	#either insert the document into an already existing point in the corpus
	try:
		df[key] += int(count)
		corp[key].append(dID)
	#or creating a new key doc pair
	except:
		df[key] = int(count)
		corp[key] = [dID]
	return corp
	
def createJSON(dID, elements, folder, corpus, df):
	#maybe open up files in append mode
	file = folder+'/'+dID+".json"
	document = {}
	for element in elements:
		#the token
		token = element['token']
		#how many of a token are in a doc
		tokenFrequency = element['tf']
		#Where a token is in a doc
		tokenPositions = element['pos']
		#adding to the total tokens in all docs
		corpus['__total__']+=tokenFrequency
		#Term frequency in a doc
		tokenFrequency = tfCalc(tokenFrequency)
		#adding a document element
		document[token] = {'tf':tokenFrequency,'count':element['tf'],'pos':tokenPositions }
		#inserting into the memory corups
		corpInsert(corpus, token, dID, df, element['tf'])
	with open(file, mode='w') as f:	
		json.dump(document,f)
	return corpus, df

def tfCalc(count):
	return 1+log10(count)

def createCorpus(corp, df, folder):
	for key in corp:
		if key is not "__total__":
			#sorting all the posting lists before final creation of the corpus
			corp[key] = sorted(corp[key], key = lambda k: int(k))
			#adding count into the corpus
			corp[key] = {'count':df[key], 'docIDs':corp[key]}
	file = folder+'/'+'__corpus__.json'
	with open(file, mode='w') as f:
		json.dump(corp,f)		
	#need to get old files and rewrite for each token every time
	
def docID(DOC):
	return DOC.split('_')[1]

def folderCheck(folderName):
	try: 
		os.stat(folderName)
	except:
		os.mkdir(folderName)