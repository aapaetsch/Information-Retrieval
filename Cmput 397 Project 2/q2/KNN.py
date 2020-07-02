import operator
import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from math import log10


class KNNmethods:
    def __init__(self):
        nltk.download('stopwords')
        self.nltk_tokenizer = RegexpTokenizer(r"\w+|\$[\d\.]+|\S+^.")
        self.stop_words = set(stopwords.words('english'))

    def tokenize(self, document):
        abstract = document['abstract']
        abstract = abstract.lower()
        docTokens = {}
        #tokenize abstract and remove stopwords
        tokens = self.nltk_tokenizer.tokenize(abstract)
        filteredTokens = [wordToken for wordToken in tokens if not wordToken in self.stop_words]
        
        for word in filteredTokens:
            if word in docTokens:
                docTokens[word] += 1
            else:
                docTokens[word] = 1

        #logged tf
        for token, count in docTokens.items():
            if count > 0:
                docTokens[token] = 1 + log10(count)
            else:
                docTokens[token] = 0

        return docTokens

    def preprocess(self, documents):
        #tokenize and return list of tokens (prob remove stop words for greater accuracy)
        docPrime = {}
        df = {}
        for doc in documents:
            docTokens = {}
            abstract = doc['abstract']
            abstract = abstract.lower()
            #tokenize abstract and remove stopwords
            tokens = self.nltk_tokenizer.tokenize(abstract)
            filteredTokens = [wordToken for wordToken in tokens if not wordToken in self.stop_words]
            
            #get tf for document
            for word in filteredTokens:
                if word in docTokens:
                    docTokens[word] += 1
                else:
                    docTokens[word] = 1

            #get tf score and add 1 to the token if it exists or add it to the df
            for token, count in docTokens.items():
                if count > 0 :
                    docTokens[token] = 1 + log10(count)
                else:
                    docTokens[token] = 0
                if token in df:
                    df[token] += 1
                else:
                    df[token] = 1

            docPrime[doc['id']] = docTokens, doc['type']
        return docPrime, df

    def computeK(self, documents):
        # compute k based off classes and documents 
        #temp usage of rule of thumb n^(1/2)
        n = len(documents)
        k = round(n**(1/2))
        #try with average of sqrt(n of each class)
        return k

    def computeNearestNeighbour(self, doc, k, df, testdoc):
        #get score of k nearest neighbour using 
        #todo 
        kneighbours = []
        N = len(doc)

        #get tf-idf for testdoc tokens
        for token, tf in testdoc.items():
            if token in df:
                testdoc[token] = tf * (log10(N/df[token]))

        #get sim score for each document
        for data in doc.values():
            training = data[0]
            trainedClass = data[1]
            score = 0
            weights = {}
            
            #get tfidf
            for token, tf in training.items():
                tfIdf = tf * log10(N/df[token])
                weights[token] = tfIdf


            for term in weights.keys():
                if term in testdoc:
                    score += testdoc[term] * weights[term]
            kneighbours.append((trainedClass,score))

        return sorted(kneighbours, key = lambda m: m[1], reverse = True )[0:k+1]

    def trainKnn(self, documents):
        doc, df = self.preprocess(documents)
        k = self.computeK(doc)
        return doc, k, df

    def applyKnn(self, documents, k, df, testDoc):
        #check sim score for each abstract with the training abstracts and return the best ones
        testDocTokens = self.tokenize(testDoc)
        neighbours = self.computeNearestNeighbour(documents, k, df, testDocTokens)
        #classDocuments = each class that occurs in neighours
        #for each class, check how many neighbours are in that class and then divide by k
        p={}
        for classj in neighbours:
            docClass = classj[0]
            docScore = classj[1]
            if docClass in p:
                p[docClass] += docScore
            else:
                p[docClass] = docScore
        return max(p.items(), key=operator.itemgetter(1))[0]
        #return p
