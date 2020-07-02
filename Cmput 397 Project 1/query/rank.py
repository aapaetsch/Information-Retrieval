def rank(weightedQuery, unrankedDocs, numDocs):

        simscores = []

        for result in unrankedDocs.keys():
                ss = 0
                nv = 0
                weightDict = {}

                # get all the weights and start to calculate
                # the normalized value along the way
                for key in unrankedDocs[result].keys():
                        weight = unrankedDocs[result][key]["tf"]
                        nv += weight ** 2
                        weightDict[key] = weight
                nv = nv ** 0.5

                # normalize the weights in the weight array
                for term in weightDict.keys():
                        weightDict[term] = weightDict[term]/nv
                #print(weightDict)
                # find the simscore of each query term
                simscore = 0
                for term in weightedQuery.keys():
                        ss += weightedQuery[term]["w"] * weightDict[term]
                simscores.append((result, ss))

        # return the sorted list of k documents to vs_query
        return sorted(simscores, key = lambda k: k[1], reverse = True )[0:numDocs]

