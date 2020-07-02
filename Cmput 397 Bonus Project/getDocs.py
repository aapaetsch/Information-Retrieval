import json
import sys



class grabDocs:
	def __init__(self, folder, tokens):
		self.__query = tokens
		self.__directory = folder
		self.__corpus = None
		self.__documents = {}

	def retrieveDocs(self):
		#gets the corpus
		self.__corpus = self.__retrieveCorpus()
		
		totalRetrieval = []
		docs = []
		for token in self.__query:
			#current implementatin takes only docs with all query tokens
			dIDs = self.__getDocIDs(token)
			if dIDs != None:
				#maybe break query if 1 term doesnt exist?
				totalRetrieval.append(dIDs)
		#if the retrieved docs is empty, exit
		if len(totalRetrieval) == 0:
			print("Error, query returned nothing. ")
			sys.exit()
		#sort the retrieved list by length of docs in each term for fastest intersect
		totalRetrieval = sorted(totalRetrieval, key = lambda x:len(x))
		if len(totalRetrieval) == 1:
			docs=totalRetrieval[0]
		else:
			#use the smallest set as the base set, if a doc isnt in it we dont need to deal with it
			smallest = totalRetrieval[0]
			for dID in smallest:
				inAll = True
				for i in range(1,len(totalRetrieval)):
					if dID in totalRetrieval[i]:
						continue
					else:
						#if a term doesnt appear in all, break
						inAll = False
						break
				if inAll:
					docs.append(dID)
		
		if len(docs) == 0:
			print('Error, query returned nothing.')
			sys.exit()

		for doc in docs:
			content = {}
			fileName = doc+'.json'
			#opens a json file based off of dID's
			allContents = self.__openJson(fileName)
			for token in self.__query:
				if token in allContents:
					#get all probabilities related to the query
					content[token] = allContents[token]['prob']

			content['__total__'] = allContents['__total__']
			content['__name__'] = allContents['__name__']
			self.__documents[doc] = content

	def getDocs(self):
		#returns the docs
		return self.__documents

	def getCorpus(self):
		#returns the corpus
		return self.__corpus

	def __getDocIDs(self, token):
		#returns a doc id of a token
		if token in self.__corpus:
			return self.__corpus[token]['dIDs']
		else:
			return None

	def __openJson(self, file):
		#open a json file
		path = self.__directory+'/'+file
		with open(path, 'r') as f:
			document = json.load(f)
		return document

	def __retrieveCorpus(self):
		#retrieve the corpus
		return self.__openJson('__corpus__.json')


