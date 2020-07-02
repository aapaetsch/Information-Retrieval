from kMeans import ecDist, calculateCentroid
import numpy as np
import random

def ecDistTest():
    v1 = np.zeros(10)
    v2 = np.zeros(10)

    for i in range(10):
        v1[i] = i
        v2[i] = 10 - i

    dist = ecDist(v1, v2)

    assert dist == 2 * np.sqrt(85)
    print("ecDist test complete")

def calculateCentroidTest():
    v1 = {'vector': np.zeros(10)}
    v2 = {'vector': np.zeros(10)}

    for i in range(10):
        v1['vector'][i] = i
        v2['vector'][i] = 10 - i

    cluster = [v1, v2]
    centroid = calculateCentroid(cluster)

    for i in centroid:
        assert i == 5
    print("calculateCentroid test complete")

ecDistTest()
calculateCentroidTest()
print("all tests complete")