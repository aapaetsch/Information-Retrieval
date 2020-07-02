from tokenizer import Tokenizer

def main():
        tkn = Tokenizer()
        testFile = "./create_index/test.txt"
        tkns = tkn.tokenize(testFile)
        testStrings = "hello my name is david how are you let s go to the store bye".split(" ")

        i = 0
        for token in tkns:
                if token["token"] != testStrings[i]:
                        raise AssertionError()
                i += 1

        print("testTokenizer passed.")


main()