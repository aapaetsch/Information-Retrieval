import os
import sys
from create_db import createDB
import nltk


def create_index(args):
	to_be_indexed = args[0]
	output_directory = args[1]
	if checkFolderExists(to_be_indexed) == False:
		print('Error, cannot create index, folder:',to_be_indexed, 'does not exist.')
		sys.exit()

	if checkFolderExists(output_directory):
		if len(os.listdir(output_directory)) != 0:
			print('Error, folder already in use. Please delete:', output_directory,' or its contents to continue.')
			sys.exit()
	else:
		createFolder(output_directory)
	#get all the files in the directory that needs to be indexed
	files = os.listdir(to_be_indexed)
	#initalize the class for creating the json files
	db = createDB(output_directory)

	for file in range(len(files)):
		try:
			if files[file].split(".")[-1] == 'txt':
				#only tokenize txt files
				
				tokens = db.tokenizeFile(to_be_indexed+'/'+files[file])
				#for each file that is tokenized, create a json file 
				db.createJson(files[file], tokens)
			
			else:
				print("File:", files[file], "is not a valid file type.")

		except:
			print('Error Indexing File:', files[file])


	db.createCorpus()

		
			

	


def checkFolderExists(folderName):
	#function to check if a folder exists
	try:
		os.stat(folderName)
		return True
	except:
		return False

def createFolder(folderName):
	#function creates a new folder
	os.mkdir(folderName)



if __name__ == '__main__':

	if len(sys.argv) == 3:
		#for downloading the proper nltk library
		nltk.download('punkt')
		create_index(sys.argv[1:])
	else:
		print("Usage: <python 3> create_index.py <Directory to be Indexed> <Output Directory>")











