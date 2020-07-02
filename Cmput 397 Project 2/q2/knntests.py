from KNN import KNNmethods
import knn_classifier


knn = KNNmethods()
def testtokenize():
    testfile = {"abstract": "testing this book with a sentence, testing test", "type": "book", "id": "193041", "title": "Pebble in the Sky"}
    testOuput = knn.tokenize(testfile)
    expectedOutput = {'testing': 1.3010299956639813, 'book':1.0, 'sentence':1.0, 'test':1.0}
    if testOuput == expectedOutput:
        return "Test document tokenizer passed"
    raise AssertionError()

def testpreprocess():
    testfile = [{"abstract": "testing this book with a sentence, testing test", "type": "book", "id": "193041", "title": "Pebble in the Sky"}, {"abstract": "test number two for preprocess", "type": "story", "id": "347543", "title": "Critique of Pure Reason"}]
    testOutput = knn.preprocess(testfile)
    expectedOutput = ({'193041': ({'testing': 1.3010299956639813, 'book': 1.0, 'sentence': 1.0, 'test': 1.0}, 'book'), '347543': ({'test': 1.0, 'number': 1.0, 'two': 1.0, 'preprocess': 1.0}, 'story')}, {'testing': 1, 'book': 1, 'sentence': 1, 'test': 2, 'number': 1, 'two': 1, 'preprocess': 1})
    if testOutput == expectedOutput:
        return "Preprocess document passed"
    raise AssertionError()

def testNeighours():
    testOutput = knn.computeNearestNeighbour({'193041': ({'testing': 1.3010299956639813, 'book': 1.0, 'sentence': 1.0, 'test': 1.0}, 'book'), '347543': ({'test': 1.0, 'number': 1.0, 'two': 1.0, 'preprocess': 1.0}, 'story')}, 3 , {'testing': 1, 'book': 1, 'sentence': 1, 'test': 2, 'number': 1, 'two': 1, 'preprocess': 1}, {'testing': 1.3010299956639813, 'book':1.0, 'sentence':1.0, 'test':1.0} )
    expectedOutput = [('book', 0.3346270980415359), ('story', 0.0)]
    if testOutput == expectedOutput:
        return "K nearest neighbours passed"
    raise AssertionError

def testAccuracy():
    testinput = {'book':{'TP':1, 'FP':0, 'FN':1}, 'building':{'TP':1, 'FP':0, 'FN':0}, 'company':{'TP':1, 'FP':0, 'FN':0}, 'country':{'TP':1, 'FP':0, 'FN':0}, 'film':{'TP':1, 'FP':1, 'FN':0}, 'game':{'TP':1, 'FP':0, 'FN':0}, 'person':{'TP':1, 'FP':0, 'FN':0}, 'school':{'TP':1, 'FP':0, 'FN':0}, 'song':{'TP':1, 'FP':0, 'FN':0}, 'stadium':{'TP':1, 'FP':0, 'FN':0}}
    testOutput = knn_classifier.accuracy(testinput)
    expectedOutput = {'book': 0.6666666666666666, 'building': 1.0, 'company': 1.0, 'country': 1.0, 'film': 0.6666666666666666, 'game': 1.0, 'person': 1.0, 'school': 1.0, 'song': 1.0, 'stadium': 1.0, 'macro': 0.9333333333333332, 'micro': 0.9090909090909091}
    if testOutput == expectedOutput:
        return "Accuracy passed"
    raise AssertionError


print(testtokenize())
print(testpreprocess())
print(testNeighours())
print(testAccuracy())