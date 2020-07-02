import nltk
from nltk.tokenize import RegexpTokenizer
import string

class Tokenizer:
        def __init__(self):
                # download nltk so its available
                nltk.download('punkt')
                self.nltk_tokenizer = RegexpTokenizer(r"\w+|\$[\d\.]+|\S+^.")

        def tokenize(self, fileName):
                tokenList = []
                # open the file and start to tokenize it
                with open(fileName, "r") as toTokenize:
                        for line in toTokenize:
                                tokenizedLine = self.nltk_tokenizer.tokenize(line.lower())
                                # for each tokenized symbol in tokenizedLine arrary, create or update a dict
                                for index, token in enumerate(tokenizedLine):
                                        # create dict
                                        tokenDict = {"token": "", "tf": 0, "pos": []}
                                        # if the token is a single character, delete it if its a symbol
                                        if len(token) == 1:
                                                token = token.translate(str.maketrans('','',string.punctuation))
                                        token = token.translate(str.maketrans("\/.", "&&,"))
                                        # create a token for adding to tokenList
                                        tempToken = token

                                        # check if the token already exists in the tokenList
                                        found = False
                                        for tkndict in tokenList:
                                                # update entry if it exists
                                                if tkndict["token"] == tempToken:
                                                        tkndict["tf"] += 1
                                                        tkndict["pos"].append(index)
                                                        # update to found = true
                                                        found = True
                                        # if the token wasn't found, create it
                                        if not found and len(token) > 0 and "'" not in token:
                                                # make contractions one word but ignore anything with "'s"
                                                if index + 1 < len(tokenizedLine) and "'" in tokenizedLine[index+1] and "'s" not in tokenizedLine[index + 1]:
                                                        tempToken = token + tokenizedLine[index + 1]
                                                tokenDict["token"] = tempToken
                                                tokenDict["tf"] = 1
                                                tokenDict["pos"].append(index)
                                        # if the tokenDict was created successfully, append it to tokenList
                                        if len(tokenDict["token"]) > 0:
                                                tokenList.append(tokenDict)

                return tokenList
