import nltk
import sys
import os
from nltk.tokenize import RegexpTokenizer
import json
from getDocs import grabDocs
import string
from math import log10


def lm_query(args):
	#arg 0 is the index directory
	indexDirectory = args[0]
	# exit if k is not an int
	try:
		k = int(args[1])
	except:
		print("Error, K:",args[1], "is not an integer.")
		sys.exit()
	printScores = None
	keywords = args[3:]
	if args[2].lower() == 'yes' or args[2].lower() == 'y':
		printScores = True
	else:
		printScores = False
	# if index check does not pass, program will exit
	indexCheck(indexDirectory)
	#tokenize all the query terms
	query = tokenizeQuery(keywords)
	if len(query) == 0:
		print('No terms in query after tokenizing, exiting program.')
		sys.exit()
	#grab the relavent docs
	grabber = grabDocs(indexDirectory, query)
	grabber.retrieveDocs()
	#call the return function for the docs grabbed
	docs = grabber.getDocs()
	#do the scoring on the docs based on the query
	getUnimodelScore(docs, query, k, printScores)




def getUnimodelScore(docs, query, k, printScores):
	#scoring uses unimodel scores
	scores = {}
	reversedScores = {}
	missing = []
	for doc in docs:
		
		for term in query:
			if term in docs[doc]:
				#use log10 to get rid of overflow errors
				try:
					scores[doc] += log10(docs[doc][term])
				except:
					scores[doc] = log10(docs[doc][term])
			else:
				if term not in missing:
						missing.append(term)
	topK = []
	for key in scores:
		reversedScores[scores[key]] = key
		topK.append(scores[key])
	topK = sorted(topK, key = lambda x:-(x))

	if len(topK) > int(k):
		topK = topK[:k]
	scoreString = ''
	for s in range(len(topK)):
		#gets the document name based off of its score, had to reverse for score sorting
		scoreString+=str(s+1)+':'
		scoreString += docs[reversedScores[topK[s]]]['__name__']

		if printScores:
			scoreString = scoreString + '\n\tscore:'+str(topK[s])

		scoreString += '\n'

	if len(missing) != 0:
			print('Terms:',missing, 'did not appear in any documents, Retrieved documents are scored excluding the missing terms.')
	if len(topK) < k:
		print('k entered higher than number of documents retrieved.')
	print(scoreString)










def tokenizeQuery(ls):
	ls = str(ls)
	#Modified from tokenizer in my groups Assignment 2 q3
	tknizer = RegexpTokenizer(r"\w+|\$[\d\.]+|\S+^.")
	#use stemming
	pStemmer = nltk.stem.porter.PorterStemmer()

	sStemmer = nltk.stem.snowball.SnowballStemmer('english')

	#make the line lowercase
	lineTokenized = tknizer.tokenize(ls.lower())

	proper = []
	for token in lineTokenized:
		tmpToken = token
		if len(tmpToken) == 1:
			#dealing with 's'
			if tmpToken in string.punctuation or tmpToken == 's':
				tmpToken = ''
		tmpToken = tmpToken.translate(str.maketrans("\/.", "&&,"))
		
		if (len(tmpToken) > 0):
			tmpToken = sStemmer.stem(pStemmer.stem(tmpToken))
			proper.append(tmpToken)
	#returns a list of tokenized terms from the query
	return proper



# def tokenizeQuery(keywords):
# 	keywords = str(keywords)
# 	tknizer = RegexpTokenizer(r"\w+|\$[\d\.]+|\S+^.")
# 	tokenizedKeywords = tknizer.tokenize(keywords.lower())
# 	return tokenizedKeywords

def indexCheck(indexDirectory):
	# checks if the index directory has files, and if so 
	# if it has a __corpus__.json file
	if checkFolderExists(indexDirectory) == False:
		print('Error, Incorrect Directory for Index.')
		sys.exit()
	else:
		if len(os.listdir(indexDirectory)) == 0:
			print('Error, Folder does not have any files!')
			sys.exit()
		elif '__corpus__.json' not in os.listdir(indexDirectory):
			print('Error, No corpus found.')
			sys.exit()

def checkFolderExists(folderName):
	#function for checking if the input folder is a real folder
	try:
		os.stat(folderName)
		return True
	except:
		return False


if __name__ == '__main__':
	if len(sys.argv) >= 5:
		#get the required nltk libraries
		nltk.download('punkt')
		#was going to use cls and clear for clearing the terminal but that would clear
		#everything to the output of lm_query, instructor might not want that
		print('\n\n\n')
		lm_query(sys.argv[1:])
	else:
		print("Usage: <python 3> lm_query.py <Directory of Index> <K> <y/n> <keywords>...")



