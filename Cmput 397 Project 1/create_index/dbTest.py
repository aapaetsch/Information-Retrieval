from math import log10
import dbCreate
def main():


	logOf12 = 2.079181246047625
	N = 12
	tests = 0
	if logOf12 == dbCreate.tfCalc(N):
		print("TF Calculation: Passed")
		tests+=1
	else:
		raise AssertionError()
	testDoc = "Doc_29_10_Black_Panther.txt"
	testID = "29"
	if testID == dbCreate.docID(testDoc):
		print("DocID: Passed")
		tests+=1
	else:
		raise AssertionError()
	if tests == 2:
		print("All db tests passed")


main()