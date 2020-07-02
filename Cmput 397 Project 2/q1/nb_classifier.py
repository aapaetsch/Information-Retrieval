import splitFile
from fractions import Fraction
from math import log10
from nbMath import NBMath
import time
import NBtest
import json
import sys, os

def nb(Files):
	trainingFile = Files[0]
	testingFile = Files[1]

	print("Starting getSets()")
	# creates subsets, vocab sets, classifiers and class list for the training file
	subsets, vocabsets, classifiersDict, classifiersList = getSets(trainingFile)
	print("Finished getSets()\n")
	accuracy = {}#dictionary for holding the accuracies (tp, fp, fn, tn)
	conditional = {}#dictionary for holding conditional probability
	subsetFeatures = {}#dictionary for holding the features for each subset
	# weights based off of the distribution of training file
	weights = {'book':2.29, 'building':2.19, 'company':3.22,'country':1.98
	, 'film':17.57,'game':0.32,'person':15.22, 'school':2.35,'song':.74, 'stadium':2.99}

	start = time.time()
	##comment out from here
	for subset in range(len(subsets)):

		accuracy[int(subset)] = {}
		for c in classifiersList:
			#populate the accuracy dictionary
			accuracy[int(subset)][c] = {'TP':0,'FP':0,'FN':0,'TN':0}

	print("Training started!")
	#for each subset, do feature selection and conditional calculations
	for subset in range(len(subsets)):
		#calculate the conditional probabilities of a subset
		conditional[int(subset)] = naiveBayesTraining(vocabsets[subset], classifiersDict[subset], subsets[subset])

		print("Finished training\n")


		# print("Starting feature selection")
		# featureSelectionStart = time.time()
		nbMath = NBMath(2500)
		# ###skip here
		features = nbMath.getFeaturesForClass(subsets[subset], classifiersList)
		# add this subsets features to subsetFeatures
		subsetFeatures[int(subset)] = features

	print("Training Completed!")




	print("Starting accuracy calculation")

	for subset in range(len(subsets)):
		current = subset

		for subset2 in range(len(subsets)):
			#if the subset is not the subset that is reserved for testing
			if current != subset2:
				#using the testing subset
				for doc in subsets[current]:

					docTokens = doc['tknzAbstract']
					#get the predicted class of the document based off one of the training sets
					prediction = NBtest.ApplyMultinomialNB(weights, classifiersList, classifiersDict[subset], subsetFeatures, docTokens, conditional[subset])
					#update function for tp, fn, fp, tn
					updateAccuracy(accuracy[current], prediction, doc['type'], classifiersList)
	print("Finished accuracy calculation")

	microMacro = {}

	print("Accuracies for Training:")
	for subset in range(len(subsets)):
		#get the micro and macro of each subset
		print('\tAccuracies when',subset, "is the testing set:")
		microMacro[subset] = {'micro': 0, 'macro': 0}
		TP = 0
		TN = 0
		FP = 0
		FN = 0
		for aClass in classifiersList:
			#get precision and recall for a class in a subset
			P = precision(aClass, accuracy[subset])
			R = recall(aClass, accuracy[subset])
			#get the overall total of tp, tn, fn, fp of a subset for a class
			TP += accuracy[subset][aClass]['TP']
			TN += accuracy[subset][aClass]['TN']
			FP += accuracy[subset][aClass]['FP']
			FN += accuracy[subset][aClass]['FN']
			F1 = getF1(P, R)
			microMacro[subset]['macro'] += F1
		#do the micro and macro calculations
		microMacro[subset]['macro'] = microMacro[subset]['macro']/len(classifiersList)
		microMacro[subset]['micro'] = getF1((TP/(TP+FP)),(TP/(TP+FN)))
		print('\t\tMacro:', microMacro[subset]['macro'])
		print('\t\tMicro:', microMacro[subset]['micro'])
	#start the best score at -1
	bestSubsetIndex = -1
	bestSubsetScore = -1
	for subset in microMacro:
		#for each subset, check if the score is higher than the best score, if so
		#the score is updated and so is the index
		if microMacro[subset]['macro'] > bestSubsetScore:
			bestSubsetScore = microMacro[subset]['macro']
			bestSubsetIndex = subset

	#call the function to tokenize the test set
	testSet = prepTest(testingFile)
	accuracy = {}
	for c in classifiersList:
		#clear the accuracy dictionary and reset it
		accuracy[c] = {'TP':0,'FP':0,'FN':0,'TN':0}
	for subset in range(len(subsets)):
		if subset != bestSubsetIndex:
			for doc in testSet:
				#if the subset is not the one identified as the best for testing(therefore the rest are the 9 best for training)
				docTokens = doc['tknzAbstract']
				#get the prediction of a document based on one of those 9 subsets
				prediction = NBtest.ApplyMultinomialNB(weights, classifiersList, classifiersDict[subset], subsetFeatures, docTokens, conditional[subset])
				# update accuracy
				updateAccuracy(accuracy, prediction, doc['type'], classifiersList)

	microMacro = {'micro': 0, 'macro': 0}
	TP = 0
	TN = 0
	FP = 0
	FN = 0
	for aClass in classifiersList:
		#get precision and recall for the test json
		P = precision(aClass, accuracy)
		R = recall(aClass, accuracy)
		#get total tp, tn, fp, fn
		TP += accuracy[aClass]['TP']
		TN += accuracy[aClass]['TN']
		FP += accuracy[aClass]['FP']
		FN += accuracy[aClass]['FN']
		F1 = getF1(P, R)
		microMacro['macro'] += F1
	#calculate macro/micro for test json
	microMacro['macro'] = microMacro['macro']/len(classifiersList)
	microMacro['micro'] = getF1((TP/(TP+FP)),(TP/(TP+FN)))
	print("For the Test File:")
	#display the micro macro for test json
	print("\t\tMacro:", microMacro['macro'],'\n\t\tMicro',microMacro['micro'])


	end = time.time()
	print("Total time: " + str(end - start))


def prepTest(fileName):
	#prep function for tokenizing the filenames
	with open(fileName,'r') as f:
		d = json.load(f)

	for doc in d:
		docTokens = splitFile.tknize(doc['abstract'])
		doc['tknzAbstract'] = docTokens

	return d

def updateAccuracy(accuracy, prediction, real, classes):
	#updating tp, fp, tn and fn for a class
	for aClass in classes:
			if prediction == aClass:
				if prediction == real:
					accuracy[aClass]['TP'] += 1
				elif prediction != real:
					accuracy[aClass]['FP'] += 1
			elif prediction != aClass:
				if prediction == real:
					accuracy[aClass]['FN'] += 1
				elif prediction != real:
					accuracy[aClass]['TN'] += 1

def precision(aClass, accuracy):
	#calculates precision from an accuracy dictionary given a class
	TP = accuracy[aClass]['TP']
	FP = accuracy[aClass]['FP']
	if TP==0 and FP ==0:
		P = 0
	else:
		P = TP/(TP+FP)
	return P

def recall(aClass, accuracy):
	#calculates recall from an accuracy dictionary given a class
	TP = accuracy[aClass]['TP']
	FN = accuracy[aClass]['FP']
	if TP == 0 and FN == 0:
		R = 0
	else:
		R = TP/(TP+FN)
	return R

def getF1(P, R):
	#given a P and R,
	num = 2 * P * R
	denom = P + R
	if denom == 0:
		F1 = 0
	else:
		F1 = num/denom
	return F1


def getSets(fileName):
	subsets, cDict = splitFile.splitter(fileName)
	classifiersList = list(cDict.keys())
	vocabsets = {}

	#only do tokenization on the first 9 subsets and do tokenization on the last subset in test
	for subset in range(len(subsets)):
		 #each subset gets a vocab set and probability? idk if this is correct
		vocabset = {}
		for document in range(len(subsets[subset])):

			docTokens = splitFile.tknize(subsets[subset][document]['abstract'])
			subsets[subset][document]['tknzAbstract'] = docTokens
			docTokens = set(docTokens)
			if document == 0:
				for i in docTokens:
					vocabset[i] = 1
			else:
				for i in docTokens:
					if i in vocabset:
						pass
					else:
						vocabset[i] = 1
		vocabsets[subset] = vocabset
	classifiersDict = {}
	for i in range(len(subsets)):
		classifiersDict[i] = cDict.copy()

	return subsets, vocabsets, classifiersDict, classifiersList


def naiveBayesTraining(V,C,D):
	#V is all unique tokens in D
	N = len(D)
	# for c in C:
	# dictionary for T
	T = {}
	classTokens = {}# { class {token:0}}
	for aClass in C:
		classTokens[aClass] = []
		T[aClass] = {}
		for token in V:
			T[aClass][token] = 1
		T[aClass]['__total__'] = len(V.keys())
	# for each document in the subset

	for doc in D:
		currentClass = doc['type']
		#add +1 to its type in C
		C[currentClass] += 1
		# to create each T, each sub T is just a list of tokenization of all docs
		# of that class
		docTokens = doc['tknzAbstract']
		classTokens[currentClass] += docTokens

	for aClass in C:
		# equal to log10(a/b)
		C[aClass] = log10(C[aClass])-log10(N)
		for token in V:
			for aToken in classTokens[aClass]:
				if aToken == token:
						T[aClass][token] += 1
						T[aClass]['__total__'] += 1

		for token in V:
			T[aClass][token] = log10(T[aClass][token])-log10(T[aClass]['__total__'])

	return T





if __name__ == '__main__':
	if len(sys.argv) == 3:
		if (os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2])):
			nb(sys.argv[1:])
		else:
			print("One or Both of the arguments given are not files.\nUsage:<python3> q1/nb_classifier.py <training file> <testing file>")
	else:
		print("Improper number of arguments given.\nUsage:<python3> q1/nbclassifier.py <training file> <testing file>")

