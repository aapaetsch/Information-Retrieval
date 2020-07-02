from tknzr import tknize, splitter
import os, sys
from random import sample
import numpy
from numpy import min, where, sqrt, square, sum, random
from kMeansTest import kMeansTest

def kMeans(sets, k):
    numpy.seterr(over='ignore')

    print("Tokenizing docs and converting to vectors")
    allDocs, classes = splitter(sets)
    print("Tokization complete\n")

    print("Gathering seeds")
    seeds = selectSeeds(allDocs, int(k))
    print("Finished gathering seeds\n")
    previousClusters = []
    currentClusters = []

    iteration = 1

    # check to see if kMeans should stop
    while iteration < 15:
        # clear current clusters list
        currentClusters = [[] for i in range(len(seeds))]

        print("     Assigning to closest centroid for iteration " + str(iteration))
        for doc in allDocs:
            assignToClosestCentroid(doc, currentClusters, seeds)
        print("     Finished assigning centroids\n")

        index = 0
        for i in currentClusters:
            print("         cluster " + str(index) + ": " + str(len(i)) + " docs")
            index += 1
        # reconstruct centroids
        print("     Reconstructing centroids for iteration " + str(iteration))
        print("     ...This will take some time.")
        seeds = []
        for c in currentClusters:
            newSeed = recalculateCentroids(c)
            if type(newSeed['vector']) == type(None):
                seeds.append(selectSeeds(allDocs, 1)[0])
            else:
                seeds.append(newSeed)
        print("     Finished reconstructing centroids\n")
        iteration += 1

    kMeansTest(currentClusters, classes, len(allDocs))


def selectSeeds(allDocs, numSeeds):
    return sample(allDocs, numSeeds)

def assignToClosestCentroid(doc, current, centroids):
    centers = []
    for centroid in centroids:
        # get vectors
        centroidVector = centroid['vector']
        docVector = doc['vector']

        # find distance between vectors
        dist = ecDist(centroidVector, docVector)

        if numpy.isnan([dist]):
            dist = numpy.inf

        centers.append(dist)
    closest = random.choice(where(centers == min(centers))[0])

    # assign doc to closest centroid
    current[closest].append(doc)

def ecDist(v1, v2):
    return sqrt(sum(square(v1 - v2)))

def recalculateCentroids(cluster):
    if len(cluster) > 0:
        centroidVector = calculateCentroid(cluster)

        return {'vector': centroidVector}
    else:
        return {'vector': None}

def calculateCentroid(vectorArray):
        centroidVector = numpy.zeros([len(vectorArray[0]['vector'])])
        # construct numpy array for centroid calculations
        for doc in (vectorArray):
            for point in range(len(doc['vector'])):
                centroidVector[point] += doc['vector'][point]

        # create a new centroid vector
        for point in range(len(centroidVector)):
            centroidVector[point] = centroidVector[point] / len(vectorArray)

        return centroidVector

if __name__ == '__main__':
    if len(sys.argv) == 3:
        if (os.path.isfile(sys.argv[1])) :
            kMeans(sys.argv[1], sys.argv[2])
        else:
            print("Set is not a file\nUsage: ./kMeans.py <path of set> <k>")
    else:
        print("Improper number of arguments given\n Usage: ./kMeans.py <path of set> <k>")