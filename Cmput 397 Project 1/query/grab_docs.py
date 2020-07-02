import json
import time
import numpy as np
from math import log10
from rank import rank

class DocGrabber:
	def __init__(self, query, path):
		self.__query = query
		self.__path = path
		self.__corpus = None

	def grab_relavent(self):
		#self.__tokenize()
		self.__getCorpus() #grabs the corpus file
		docDict = {}
		completedRetrieval = {} #dictionary of all retrieved items in all retrieved docs to be returned by method
		phrases = {} # dictionary for the phrase queries
		for i in self.__query:
			if " " not in i:
				x = self.__getDocs(i)
				if x != None:
					docDict[i] = x

			else:

				similarDocs = self.__handlePhrase(i)#get the relevant documents for phrase queries
				if similarDocs != None: # if a phrase query has a match
					phrases[i] = similarDocs
		docTokens = {}
		temp = [] #temp list with all documents
		for i in docDict:#add all documents for each term to temp
			temp+=docDict[i]
		for key in phrases:#add all documents for each phrase to temp
			temp += phrases[key]
		allDocs = np.unique(temp)#get the unique documents
		jacyDocs = {}
		for i in allDocs: #if a doc has hits from the query
			
			with open(self.__path+i+'.json', 'r') as f:#open the doc
				document = json.load(f)
			retrieved = {} #retrieved tokens keys are doc ids
			add = False
			

			for token in self.__query:
				
				if " " not in token:# for handling single word query items
					if token in document:
						retrieved[token] = {'tf':document[token]['tf']}#add tf if there is a hit
						
						add = True
					else:
						
						retrieved[token] = {"tf":0}#add only tf if no hit
						
				else:#for handling phrase queries
					if token in phrases:#if a token is a phrase query where both sub tokens exist in a docs
						
						if i in phrases[token]:
							
							
							retrieved[token], jacyDocs[token] = self.__calcPhrase(document, token)#calculates tf of the prase query
							
							if retrieved[token]['tf'] != 0 :
								add = True
								
							phrases[token].remove(i)#remove the docs already accessed
							
						else:
							retrieved[token] = {'tf':0}
					else:
						retrieved[token] = {'tf':0}
				
			if add:
				completedRetrieval[i] = retrieved#adds the retrieved info to the specific document
		
		return completedRetrieval, jacyDocs

	def __calcPhrase(self, document, token):
		# only doing for 2 term for now
		tokens = token.split(' ')
		hits = 0
		first = document[tokens[0]]

		subtokens = len(tokens)
		Max = len(first['pos'])
		for i in range(Max):
			sequental = True
			position = first['pos'][i]#where the first subtoken is
			for j in range(1,subtokens):#for each subtoken
				if position + 1 in document[tokens[j]]['pos']:#check if the next subtoken is next in pos
					position += 1#increment the position
				else:
					sequental = False#the tokens are not sequental
					break
			if sequental:#if they are sequental
				hits += 1#add 1 to hits
		
		if hits != 0:#do the tf calculation if they are sequental
			tf = 1+log10(hits)
			return {'tf':tf}, {'count':hits}
		else:
			return {'tf':0},{'count':0}#return 0 of no hits


	def __handlePhrase(self, phrase):
		listPhrase = phrase.split(' ')#split the phrase into sub tokens
		allDocs = []#list for holding all the documents retrieved for each sub token
		for i in listPhrase:
			allDocs.append(self.__getDocs(i))
		if None in allDocs:
			return None
		allDocs = sorted(allDocs, key = lambda x:len(x))#sort for the shortest list of documents
		similarDocs = []#list for documents that are similar
		#this can be simplified if phrase queries are only 2 long
		if len(allDocs) == len(listPhrase):
			#checks for matching documents for all items in the phrase query
			for i in allDocs[0]:
				match = True
				for j in range(len(allDocs)):
					if ((j != 0) and i not in allDocs[j]):
						match = False
						break
				if match == True:
					similarDocs.append(i)
			#returns the similar documents only if there are similar documents
			if len(similarDocs)!=0:
				return similarDocs
			else:
				return None
		else:
			return None

	def __getCorpus(self):
		#load the corpus into the class
		corpus = self.__path+'__corpus__.json'
		with open(corpus,'r') as f:
			self.__corpus = json.load(f)

	def __getDocs(self, token):
		#returns the doc ids of a token if that token has hits
		if token in self.__corpus:
			return self.__corpus[token]['docIDs']
		else:
			return None

