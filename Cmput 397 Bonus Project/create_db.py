from math import log10
import nltk 
from nltk.tokenize import RegexpTokenizer
import string
import json

class createDB:
	def __init__(self, folderName):
		
		self.__corpus = {'__total__':0}
		self.__folderName = folderName
		self.__tknizer = RegexpTokenizer(r"\w+|\$[\d\.]+|\S+^.")

	def tokenizeFile(self, file):
		#change this to implement the a2 version
		document = {'__total__':0}
		with open(file, 'r') as f:
			for line in f:
				lineTokenized = self.__stemmerTknizer(line)
				#for each line in a document to be indexed, tokenize then try to add
				#each token to the document, if not create a new entry
				for i in range(len(lineTokenized)):
					token = lineTokenized[i]
					try:
						document[token]['tf'] += 1
						document[token]['pos'].append(i)
						document['__total__'] +=1
					except:
						document[token] = {"tf": 1 , "pos":[i]}
						document['__total__'] += 1
		return document

	def __stemmerTknizer(self, ls):
		#Modified from tokenizer in my groups Assignment 2 q3

		pStemmer = nltk.stem.porter.PorterStemmer()
		sStemmer = nltk.stem.snowball.SnowballStemmer('english')
		# stopWords = list(set(nltk.corpus.stopwords.words('english')))
		lineTokenized = self.__tknizer.tokenize(ls.lower())
		proper = []
		for token in lineTokenized:
			tmpToken = token
			if len(tmpToken) == 1:
				if tmpToken in string.punctuation or tmpToken == 's':
					tmpToken = ''
			tmpToken = tmpToken.translate(str.maketrans("\/.", "&&,"))
			
			if (len(tmpToken) > 0):
				
				tmpToken = sStemmer.stem(pStemmer.stem(tmpToken))
				proper.append(tmpToken)
		return proper

	def createJson(self, fileName, docContents):
		#use the doc id to set the json name
		dID = self.__getDocID(fileName)

		filePath = self.__folderName+'/'+dID+'.json'
		document = {'__total__':docContents['__total__'], '__name__':fileName}
		for token in docContents:
			if token != '__total__' and token != '__name__':
				#get the term frequency, positions and total terms in a document
				tf = docContents[token]['tf']
				pos = docContents[token]['pos']
				docTotal = docContents['__total__']
				self.__corpus['__total__'] += tf
				#get the probability for a token
				document[token] = {'prob':self.__getProb(tf, docTotal),'count':tf, 'pos':pos}
				self.__updateCorp(token, dID) #update the corpus with the new indexed data
		#save a json file
		self.__saveToFile(filePath, document)

	def createCorpus(self):
		#method for creating the corpus
		file = self.__folderName + '/' + '__corpus__.json'
		for key in self.__corpus:
			if key is not "__total__":
				#each corpus entry by token needs a list of sorted doc ID's
				self.__corpus[key] = {'dIDs':sorted(self.__corpus[key], key = lambda d: int(d)),
				'count': len(self.__corpus[key])}
		self.__saveToFile(file, self.__corpus)

	def __updateCorp(self, key, docID):
		#method for updating the corpus
		try:
			self.__corpus[key].append(docID)
		except:
			self.__corpus[key] = [docID]

	def __getProb(self,count, total):
		#method for getting probability
		return count/total

	def __getDocID(self, DOC):
		#split out the document IDs
		return DOC.split('_')[1]

	def __saveToFile(self, file, contents):
		#method to save to a json file 
		with open(file, mode="w") as f:
			json.dump(contents, f)