import operator as op
from functools import reduce

def kMeansTest(clusters, classes, numDocs):
    classDict = {}

    for i in range(len(clusters)):
        classDict[i] = {}
        for c in classes:
            classDict[i][c] = 0

    for cluster in range(len(clusters)):
        for doc in clusters[cluster]:
            for c in classes:
                if doc['type'] == c:
                    classDict[cluster][c] += 1
                    break

    purity = calculatePurity(classDict, numDocs)
    RI = calculateRI(clusters, numDocs)

    print("The purity is : " + str(purity))
    print("The Rand Index is : " + str(RI))


def calculateRI(clusters, numDocs):
    TPTN = 0
    for cluster in clusters:
        TPTN += nCr(len(cluster), 2)
    return TPTN / nCr(numDocs, 2)

def calculatePurity(classDict, numDocs):
    maxes = []
    for cluster in classDict.keys():
        clusterClass = max(classDict[cluster].keys(), key=(lambda k: classDict[cluster][k]))
        maxes.append(classDict[cluster][clusterClass])

    return (1/numDocs) * sum(maxes)

def nCr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom