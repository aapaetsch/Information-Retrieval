import sys
import os
import json
from mrjobcreate import MRIndexCreatorCorpus, MRIndexCreator
#from mapper import Mapper
#from reducer import Reducer

#taken from dbCreate since importing between files doesnt work in python
def folderCheck(folderName):
	try: 
		os.stat(folderName)
	except:
		os.mkdir(folderName)

def create_index(argv):
    folderCheck(argv[1])
    #run mapreducer for corpus file
    mr_job = MRIndexCreatorCorpus(args=[argv[0]]) #if hadoop was implemented args '-r', 'hadoop' would be added here
    with mr_job.make_runner() as runner:
        runner.run() # run the mapreduce job for create corpus
        for line in runner.cat_output():
            #gets the output from mapreduce and writes it to json
            key, value = mr_job.parse_output_line(line)
            file = argv[1] + "/__corpus__.json"
            with open(file, mode='w') as f:
                json.dump(value,f)
    
    #run mapreducer for index files
    mr_job = MRIndexCreator(args=[argv[0]]) #if hadoop was implemented args '-r', 'hadoop' would be added here
    with mr_job.make_runner() as runner:
        runner.run() #run the mapreduce job for create index
        for line in runner.cat_output():
            try:
                key, value = mr_job.parse_output_line(line)
                #gets the output from each reduce process and writes it to its corresponding docID.json
                file = argv[1] +"/" + str(key) + ".json"
                with open(file, mode='w') as f:
                    json.dump(value,f)
            except:
                pass
        

if __name__=='__main__':
    if len(sys.argv) == 3:
        create_index(sys.argv[1:])
    else:
        print("Usage: ./create_index.py <corpus dir> <output file>\n")