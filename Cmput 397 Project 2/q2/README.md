
# Don't forget to:

1. Document and justify your design choices

Instructions:

1. If NLTK has not already been installed, run 'pip3 install nltk'
2. To run K Nearest Neighbours classifier, use 'python3 q2/knn_classifier.py <path to training json> <path to testing json>

We chose to use cosine similarity on tf-idf weights over euclidian distance as it better relates documents to their neighbours. We also chose not to use stemming or lemmatization in KNN as it resulted in a lower F1 accuracy. 
We find the optimal K by running the algorithm using k = every odd number up to [number of training documents] ** 0.5 or up to the optimal K. The optimal K is decided when the accuracy no longer increases and begins to fall. 
Max K of [number of training documents] ** 0.5 is used as our researched showed that n ** 0.5 is a good rule of thumb to use for KNN classification.