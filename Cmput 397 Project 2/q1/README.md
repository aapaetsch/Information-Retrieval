
# Don't forget to:

1. Make sure your program does not use class labels to build models
1. Make sure your program does not mix training and testing documents
1. Make sure you document your choice of model and feature selection
1. Decide and document how you deal with class imbalance

- Using Mutual Information as our feature selection method because we are doing multinomial naive bayes
- We decided on using 2500 features as it provided the best tested accuracy (experimentation)
- We weight based on a (numDocs in class)/100
- unit tests can be run with ```<python3> tests_for_nb.py```
- running nb_classifier is done by ```<python3> q1/nb_classifier.py <train.json file> <test.json file>```

