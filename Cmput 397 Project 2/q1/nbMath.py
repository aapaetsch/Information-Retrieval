from splitFile import tknize
from math import log2

class NBMath:
    def __init__(self, k):
        self.__k = k

    def getFeaturesForClass(self, D, C):
        # D is the set of docs
        # C is the set of classes
        # V is the set of vocabs of the docs
        classFeatures = {}
        classVocab = {}

        
        for c in C:
            classVocab[c] = []
            for d in D:
                if d['type'] == c:
                    classVocab[c].append(set(d['tknzAbstract']))
            # print("     Starting featureSelection for class " + c)
            L = []
            for docVocab in classVocab[c]:
                for term in docVocab:
                    featureUtility = self.featureSelection(term, D, C)
                    L.append({'feature':term, 'featureUtility':featureUtility})
            maxFeatures = self.__k
            if self.__k > len(L):
                maxFeatures = len(L)

            sortedL = sorted(L, key = lambda k:k['featureUtility'], reverse = True)[0:maxFeatures]
            classFeatures[c] = sortedL
            
            
        return classFeatures


    def featureSelection(self, t, D, C):
        # t is the term to determine if it should be selected
        # as a feature
        # D is the set of docs
        # C is the list of classes

        # assign to zero for smoothing
        N00 = 1 # doc does not contain t and is not part of the class
        N10 = 1 # doc contains t and is not part of the class
        N01 = 1 # doc does not contain t and is part of the class
        N11 = 1 # doc contains t and is part of the class
        N0dot = 1 # doc does not contain t
        Ndot0 = 1 # doc is not part of the class
        Ndot1 = 1 # doc is part of the class
        N1dot = 1 # doc contains t
        for c in C:
            for doc in D:
                abstract = doc['tknzAbstract']
                docClass = doc['type']
                if docClass == c: # doc is part of class
                    Ndot1 += 1
                    if t in abstract: # doc has t and is part of class
                        N11 += 1
                        N1dot += 1
                    else: # doc does not have t and is part of class
                        N01 += 1
                        N0dot += 1
                else: # doc is not part of the class
                    Ndot0 += 1
                    if t in abstract: # doc has t and is not part of class
                        N10 += 1
                        N1dot += 1
                    else: # doc does not have t and is not part of the class
                        N00 += 1
                        N0dot += 1

        N = N00 + N01 + N0dot + N10 + N11 + N1dot + Ndot0 + Ndot1

        # convert division to subtraction using log to avoid divide by zero errors
        I = (N11 / N) * log2(N * N11) - log2(N1dot * Ndot1) + \
            (N01 / N) * log2(N * N01) - log2(N0dot * Ndot1) + \
            (N10 / N) * log2(N * N10) - log2(N1dot * Ndot0) + \
            (N00 / N) * log2(N * N00) - log2(N0dot * Ndot0)

        return I