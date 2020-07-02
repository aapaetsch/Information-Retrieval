import os, sys, json
from KNN import KNNmethods
import time

def accuracy(F1):
    microTP = 0
    microFP = 0
    microFN = 0
    macro = []
    accuracyDict = {}
    for className,posNeg in F1.items():
        microTP += posNeg['TP']
        microFP += posNeg['FP']
        microFN += posNeg['FN']
        #divide by zero when TP and FP or FN are both 0 so make precision/recall 0 if no TP or FP/FN
        #calculate precision
        if posNeg['TP'] == 0 and posNeg['FP'] == 0:
            precision = 0
        else:
            precision = posNeg['TP']/(posNeg['TP'] + posNeg['FP'])
        #calculate recall
        if posNeg['TP'] == 0 and posNeg['FN'] == 0:
            recall = 0
        else:
            recall = posNeg['TP']/(posNeg['TP'] + posNeg['FN'])
        #calculate F
        if precision == 0  and recall == 0:
            F = 0
        else:
            F = (2*precision*recall)/(precision + recall)
        
        macro.append(F)
        accuracyDict[className] = F
    precision = microTP/(microTP + microFP)
    recall = microTP/(microTP + microFN)
    F = (2*precision*recall)/(precision + recall)
    accuracyDict["macro"] = sum(macro)/len(macro)
    accuracyDict["micro"] = F
    return accuracyDict

def knnRun(argv):
    timeStart = time.time()
    #downloads nltk stopwords if needed, loads stopword aand loads regex
    knn = KNNmethods()
    #open training json and preprocess it
    with open(argv[0],'r') as f:
        d = json.load(f)
    print("training")
    preprocess, k, df = knn.trainKnn(d)
    training = time.time()
    print("training time: ",training-timeStart)
    
    #open test json for applying knn
    with open(argv[1],'r') as f:
        test = json.load(f)
    #prediction = computeNearestNeighbour(preprocess, k, df, toTest)
    #print(prediction)
    F1 = {}
    currbest = 0
    bestK = 0
    bestAcc = {}
    for kval in range(1,k,2):
        print("PREDICTING FOR K=", kval)
        for toTest in test:
            #using rule of thumb k here but with this test set k=25 got best accuracy of macro:65.3% & micro:62.8%
            prediction = knn.applyKnn(preprocess, kval, df, toTest)
            #true positives, predicted to be in class and in class
            
            if prediction == toTest['type']:
                if toTest['type'] in F1:
                    F1[toTest['type']]['TP'] += 1
                else:
                    F1[toTest['type']] = {'TP':1, 'FP':0, 'FN':0}
            #predicted to be in a class that is not the class of the doc
            else:
                if prediction in F1:
                    F1[prediction]['FP'] += 1
                    #cover false negatives
                    if toTest['type'] in F1:
                        F1[toTest['type']]['FN'] += 1
                    else:
                        F1[toTest['type']] = {'TP':0, 'FP':0, 'FN':1}   
                else:
                    F1[prediction] = {'TP':0, 'FP':1, 'FN':0}
                    #cover false negatives
                    if toTest['type'] in F1:
                        F1[toTest['type']]['FN'] += 1
                    else:
                        F1[toTest['type']] = {'TP':0, 'FP':0, 'FN':1}
        accuracyd = accuracy(F1)
        if currbest < max(accuracyd['macro'],accuracyd['micro']):
            currbest = max(accuracyd['macro'], accuracyd['micro'])
            bestK = kval
            bestAcc = accuracyd
        else:
            break
    print("best Accuracy at {}% with k value of {}" .format(currbest*100, bestK))
    for k,v in bestAcc.items():
        print("\t {} : {}".format(k, v))
    full = time.time()
    print("Full Run: ", full-timeStart)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        if (os.path.isfile(sys.argv[1])) and (os.path.isfile(sys.argv[2])) :
            knnRun(sys.argv[1:])
        else:
            print("one/both of testing or training are not files\nUsage: ./q2/knn_classifier.py <path of training set> <path of testing set")
    else:
        print("Improper number of arguements given\n Usage: ./q2/knn_classifier.py <path of training set> <path of testing set")