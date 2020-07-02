
# Don't forget to:

1. Evaluate your algorithm with small collections.
1. Experiment with different values of k, computing the scores by hand in each case.

We experimented with 10 clusters, which seemed to give alright results (consistently ~55% purity). We randomize the seeds to choose, and in order to ensure that clusters of zero length do not interfere with calculations, if a cluster with no vectors is created, we re-assign that vector to a random seed. While this eliminates the guarantee of convergence, it has very little effect on the overall computation and allows the system to not crash. We choose to simply run 15 iterations of kMeans because other implementations of choosing when to stop did not have that great of an effect on the purity or rand index.

nCr implemented from https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python

To run, from main directory use `python3 ./q3/kMeans.py <set to test> <number of means>`

To run unit tests, use `python3 ./q3/unitTests.py`