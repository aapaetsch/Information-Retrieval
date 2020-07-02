from math import log10
import operator

def ApplyMultinomialNB(weights, classSet, prior, feature, docTest, conditional):
    #classSet is list of all classes
    #prior is dict of classes with prior
    #feature is the dict of dicts of feature tokens and feature utility
    # docTest is the list of tokens in the testing doc
    #if we go dict method only send keys to extracttokensfromdoc using dict.keys

    score = {}
    for c in classSet:
        score[c] = prior[c]

    for c in classSet:
    #for each class in classSet compute its score and adjust based on prior and feature utility

        for term in docTest:
            for id, features in feature.items():
            #get feature dict of each subset
                for featureCheck in features[c]:
                #check each {feature:token, featureUtility: float} if its the term we are checking and add it to score if in feature
                    if featureCheck['feature'] == term:
                        if term in conditional[c]:
                            score[c] += conditional[c][term]
                        else:
                            for c in classSet:
                                score[c] += 1
        score[c] = weights[c]*score[c]

    return  (min(score.items(), key=operator.itemgetter(1))[0])

