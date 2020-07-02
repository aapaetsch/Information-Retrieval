import nb_classifier 

print("NB tests for F1, Recall and Precision")
testAccuracy = {'person':{'TP':1, 'FP':1,'TN':1,'FN':1}}



for aClass in testAccuracy:
	P = nb_classifier.precision(aClass, testAccuracy)
	R = nb_classifier.recall(aClass, testAccuracy)
	F1 = nb_classifier.getF1(P, R)
	if P == 0.5:
		print("P Passed!")	
	if R == 0.5:
		print("R Passed")
	if F1 == 0.5:
		print("F1 Passed!")
	if P == 0.5 and F1 == 0.5 and R == 0.5:
		print('All Tests Passed!')