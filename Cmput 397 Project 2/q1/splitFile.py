import json
import os, psutil
from random import shuffle
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

nltk.download('stopwords')

def getRam(message):
	pid = os.getpid()
	py = psutil.Process(pid)
	print(message, py.memory_info()[0]/2.**30)



def splitter(fileName):

	with open(fileName,'r') as f:
		d = json.load(f)
	#assuming the file is evenly divisable by 10
	for i in range(3):
		shuffle(d)
	subsetLength = round(len(d)/10)
	subsets = [[] for i in range(10)]
	classifiers = {}

	while True:

		for i in range(10):
			if len(d) == 0:
				break
			subsets[i].append(d.pop())
		if len(d) == 0:
			break
	#
	for subset in subsets:
		for key in subset:
			if key['type'] not in classifiers:
				classifiers[key['type']] = 1

	return subsets, classifiers

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

